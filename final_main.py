"""
final_main.py (UPDATED v3)
Single entrypoint for Crypto Portfolio Manager (Infosys Springboard).
This version adds an automatic fix: if CSV has 'daily_return' instead of 'close',
the script will rename it and continue. This avoids manual CSV edits.
Author: Generated for Anand Kumar Mandal
Contact: anandkumarmandal708@gmail.com
"""

import os, sys
import warnings
warnings.filterwarnings("ignore")

# ---- Safe imports with fallbacks ----
def safe_import(mod_name_variants):
    for name in mod_name_variants:
        try:
            mod = __import__(name)
            print(f"[INFO] Imported module: {name}")
            return mod
        except Exception:
            continue
    return None

rules_mod = safe_import(["rules"])
portfolio_mod = safe_import(["portfolio"])
stress_mod = safe_import(["stress_test", "stress_test_full"])
database_mod = safe_import(["database"])
predictor_mod = safe_import(["predictor"])
db_portfolio_mod = safe_import(["DB_portfolio", "db_portfolio"])
mail_mod = safe_import(["mailSending", "mail_sending", "mail"])

get_weights_risk_parity = getattr(rules_mod, "get_weights_risk_parity", None)
PortfolioClass = getattr(portfolio_mod, "Portfolio", None)
apply_shock = getattr(stress_mod, "apply_shock", None) if stress_mod is not None else None
save_portfolio_returns = getattr(database_mod, "save_portfolio_returns", None)
predictor = predictor_mod
add_alert = getattr(db_portfolio_mod, "add_alert", None) if db_portfolio_mod else None
send_alert = getattr(mail_mod, "send_alert", None) if mail_mod else None
ai_alert = getattr(mail_mod, "ai_alert", None) if mail_mod else None

import pandas as pd, sqlite3

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def find_csv_candidate():
    candidates = [
        "data/Crypto_metrics_daily.csv",
        "Crypto_metrics_daily.csv",
        "data/sample_prices.csv",
        "sample_prices.csv"
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    for f in os.listdir("."):
        if f.lower().endswith(".csv") and "crypto" in f.lower():
            return f
    return None

def load_combined(path=None):
    if path is None:
        path = find_csv_candidate()
    if path is None:
        raise FileNotFoundError("No CSV found. Place Crypto_metrics_daily.csv in project root or data/")
    print(f"[INFO] Loading CSV: {path}")
    df = pd.read_csv(path)
    # Normalize column names
    col_map = {}
    lower_map = {c.lower(): c for c in df.columns}
    if "asset" not in [c.lower() for c in df.columns]:
        for alt in ("symbol", "ticker", "asset_name"):
            if alt in lower_map:
                col_map[lower_map[alt]] = "asset"
                break
    if "close" not in [c.lower() for c in df.columns]:
        for alt in ("close_price", "price", "last_price"):
            if alt in lower_map:
                col_map[lower_map[alt]] = "close"
                break
    if "date" not in [c.lower() for c in df.columns]:
        for alt in ("timestamp", "time", "datetime"):
            if alt in lower_map:
                col_map[lower_map[alt]] = "date"
                break
    # New auto-fix: map 'daily_return' to 'close' if present
    if "daily_return" in lower_map and "close" not in [c.lower() for c in df.columns]:
        col_map[lower_map["daily_return"]] = "close"
        print("[INFO] Detected 'daily_return' column — mapping it to 'close' automatically.")
    if col_map:
        df = df.rename(columns=col_map)
        print(f"[INFO] Renamed columns: {col_map}")
    lower_cols = [c.lower() for c in df.columns]
    if not ("asset" in lower_cols and "close" in lower_cols):
        print("[ERROR] CSV is missing required columns. Found columns:", df.columns.tolist())
        raise ValueError("CSV must include 'asset' and 'close' columns (or synonyms like ticker/price/daily_return).")
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    else:
        df["date"] = pd.date_range(end=pd.Timestamp.today(), periods=len(df))
        print("[WARN] 'date' column missing; generated sequential dates.")
    return df

def save_portfolio_sql(df, db_path=os.path.join(RESULTS_DIR, "portfolio_returns.db")):
    conn = sqlite3.connect(db_path)
    df.to_sql("portfolio_returns", conn, if_exists="replace", index=True)
    conn.close()
    print(f"[INFO] Saved portfolio returns to {db_path}")

def run_risk_parity(df):
    if get_weights_risk_parity is None or PortfolioClass is None:
        print("[WARN] Risk-Parity or Portfolio modules not available. Skipping this step.")
        return None, None
    assets = sorted(df["asset"].unique())
    weights = get_weights_risk_parity(assets, df, window=90)
    print("[INFO] Calculated Risk-Parity weights:")
    for a,w in weights.items():
        print(f"  {a}: {w:.4f}")
    p = PortfolioClass(df)
    port_ret = p.run(weights)
    if save_portfolio_returns:
        try:
            save_portfolio_returns(port_ret)
            print("[INFO] Saved via database.save_portfolio_returns()")
        except Exception as e:
            print("[WARN] database.save_portfolio_returns failed:", e)
            save_portfolio_sql(port_ret)
    else:
        save_portfolio_sql(port_ret)
    return port_ret, weights

def run_stress_test(df, weights):
    if apply_shock is None or PortfolioClass is None:
        print("[WARN] Stress test module not available. Skipping.")
        return None
    shock_date = df["date"].iloc[len(df)//2] if "date" in df.columns else df.index[len(df)//2]
    assets = sorted(df["asset"].unique())
    shock_map = {a: -0.20 for a in assets}
    shocked = apply_shock(df, shock_date, shock_map)
    p_shocked = PortfolioClass(shocked)
    shocked_ret = p_shocked.run(weights)
    print(f"[INFO] Stress test (-20%) sample output:")
    print(shocked_ret.head())
    return shocked_ret

def run_predictor():
    if predictor is None:
        print("[WARN] predictor module not available. Skipping predictions.")
        return None
    try:
        dfp = predictor.load_data_from_csvs()
        results = predictor.run_all_predictions(dfp)
        if hasattr(predictor, "store_predictions") and results:
            try:
                predictor.store_predictions(results)
            except Exception as e:
                print("[WARN] Storing predictions failed:", e)
        return results
    except Exception as e:
        print("[ERROR] Prediction run failed:", e)
        return None

def run_risk_checks(port_ret=None):
    risk_mod = safe_import(["Risk_checker", "risk_checker", "RiskChecker"])
    if risk_mod is None:
        print("[WARN] Risk checker module not found. Skipping risk rules.")
        return None
    try:
        results = risk_mod.run_all_rules()
    except Exception as e:
        print("[ERROR] Running risk rules failed:", e)
        return None
    any_fail = False
    for rname, passed, val in results:
        print(f"Rule {rname}: passed={passed}, value={val}")
        if not passed:
            any_fail = True
            if add_alert:
                try:
                    add_alert(rname, str(val))
                except Exception:
                    pass
            if send_alert:
                try:
                    send_alert(f"Risk Alert: {rname}", str(val))
                except Exception:
                    pass
            if ai_alert:
                try:
                    ai_alert(rname, str(val), {"rule": rname})
                except Exception:
                    pass
    if any_fail:
        print("[INFO] One or more risk rules failed. Alerts attempted.")
    else:
        print("[INFO] All risk rules passed.")
    return results

def main():
    print("=== Crypto Portfolio Manager (Final Main v3) ===")
    try:
        df = load_combined()
    except Exception as e:
        print("[FATAL] Failed to load CSV:", e)
        print("Please ensure a CSV with 'asset' and 'close' columns exists in project root or data/ folder.")
        return
    if "asset" not in df.columns or "close" not in df.columns:
        print("[FATAL] Required columns missing after load. Columns found:", df.columns.tolist())
        return
    try:
        port_ret, weights = run_risk_parity(df)
    except Exception as e:
        print("[ERROR] Risk-Parity step failed:", e)
        port_ret, weights = None, None
    try:
        if weights is not None:
            _ = run_stress_test(df, weights)
    except Exception as e:
        print("[ERROR] Stress test failed:", e)
    try:
        _ = run_predictor()
    except Exception as e:
        print("[ERROR] Predictor error:", e)
    try:
        _ = run_risk_checks(port_ret)
    except Exception as e:
        print("[ERROR] Risk check error:", e)
    print("=== Demo Complete ===")
    print(f"Check the {RESULTS_DIR}/ folder and SQLite DB files for outputs.")

if __name__ == '__main__':
    main()
