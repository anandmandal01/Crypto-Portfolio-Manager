# predictor.py
# Advanced prediction module: Predict both individual assets and portfolio returns
# using Linear Regression model. Also calculates daily returns (percentage change).

import pandas as pd
import numpy as np
import sqlite3
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime
from pathlib import Path

def load_data_from_csvs():
    """Load Binance or Portfolio CSVs. If not found, generate synthetic demo data."""
    files = {
        "BTC": Path("Binance_BTCUSDT_d.csv"),
        "ETH": Path("Binance_ETHUSDT_d.csv"),
        "LTC": Path("Binance_LTCUSDT_d.csv"),
    }
    df = None
    found = False

    for k, p in files.items():
        if p.exists():
            tmp = pd.read_csv(p)
            cols_lower = [c.lower() for c in tmp.columns]
            if "close" in cols_lower:
                col = tmp.columns[cols_lower.index("close")]
                prices = pd.to_numeric(tmp[col], errors="coerce").fillna(method="ffill").fillna(0)
            else:
                numeric_cols = tmp.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    prices = pd.to_numeric(tmp[numeric_cols[0]], errors="coerce").fillna(method="ffill").fillna(0)
                else:
                    continue
            series = prices.pct_change().fillna(0)
            colname = f"{k}_pct_change"
            if df is None:
                df = pd.DataFrame({colname: series})
            else:
                df[colname] = series
            found = True

    # Portfolio file check
    portfolio_paths = [
        Path("portfolio_vs_assests.csv"),
        Path("portfolio_vs_assests_15days_equal.csv"),
        Path("Portfolio_vs_assests_(Cumulative Return         ).csv")
    ]
    for p in portfolio_paths:
        if p.exists():
            tmp = pd.read_csv(p)
            candidates = [c for c in tmp.columns if "portfolio" in c.lower() and ("pct" in c.lower() or "change" in c.lower())]
            if candidates:
                col = candidates[0]
                df["Portfolio_pct_change"] = pd.to_numeric(tmp[col], errors="coerce").fillna(0)
                found = True

    if not found or df is None:
        rng = np.random.RandomState(42)
        n = 2000
        df = pd.DataFrame({
            "BTC_pct_change": rng.normal(0, 1, size=n).cumsum(),
            "ETH_pct_change": rng.normal(0, 1.2, size=n).cumsum(),
            "LTC_pct_change": rng.normal(0, 1.1, size=n).cumsum(),
        })
        df["Portfolio_pct_change"] = (
            0.5 * df["BTC_pct_change"] +
            0.3 * df["ETH_pct_change"] +
            0.2 * df["LTC_pct_change"]
        )

    return df

def train_and_predict_series(series, label):
    y = np.asarray(series).astype(float)
    N = len(y)
    if N == 0:
        return None

    X_full = np.arange(N).reshape(-1, 1)
    model = LinearRegression()
    model.fit(X_full, y)
    y_pred_full = model.predict(X_full)

    mse = mean_squared_error(y, y_pred_full)
    r2 = r2_score(y, y_pred_full)

    last_n = min(10, N)
    actual_last = y[-last_n:]
    pred_last = y_pred_full[-last_n:]

    return {
        "label": label,
        "mse": float(mse),
        "r2": float(r2),
        "actual_last": actual_last.tolist(),
        "pred_last": pred_last.tolist(),
    }

def run_all_predictions(df):
    results = {}
    cols = [c for c in df.columns if c.lower().endswith("_pct_change") or "portfolio" in c.lower()]
    if not cols:
        print("No suitable columns found.")
        return results

    for c in cols:
        res = train_and_predict_series(df[c].fillna(0), c)
        if res is None:
            continue
        results[c] = res
        print(f"--- {c} ---")
        print(f"MSE: {res['mse']:.4f} R²: {res['r2']:.4f}")
        display_df = pd.DataFrame({
            "Asset": [c]*len(res["actual_last"]),
            "Actual": np.round(res["actual_last"], 6),
            "Predicted": np.round(res["pred_last"], 6)
        })
        print(display_df.to_string(index=False))
        print()
    return results

def store_predictions(results, db_path="crypto.db"):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS predictions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, asset TEXT, mse REAL, r2 REAL, ts TIMESTAMP)""")
    c.execute("""CREATE TABLE IF NOT EXISTS prediction_rows
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, asset TEXT, actual REAL, predicted REAL, ts TIMESTAMP)""")
    for asset, vals in results.items():
        c.execute("INSERT INTO predictions(asset, mse, r2, ts) VALUES (?, ?, ?, ?)",
                  (asset, vals["mse"], vals["r2"], datetime.utcnow().isoformat()))
        for a, p in zip(vals["actual_last"], vals["pred_last"]):
            c.execute("INSERT INTO prediction_rows(asset, actual, predicted, ts) VALUES (?, ?, ?, ?)",
                      (asset, float(a), float(p), datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()
    print("Predictions stored in DB.")

if __name__ == "__main__":
    print("Loading data...")
    df = load_data_from_csvs()

    # Show daily returns sample
    print("\n🔹 Sample Daily Returns (first 5 rows):")
    print(df.head())

    print("\nRunning predictions...")
    results = run_all_predictions(df)

    if results:
        print("Storing predictions to DB...")
        store_predictions(results)
    print("Done.")

