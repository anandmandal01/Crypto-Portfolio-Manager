import os
import yfinance as yf
import pandas as pd
import sqlite3

# ---------------------------
# 1. Create Folder with Your Name
# ---------------------------
folder_name = "Anand_Kumar_Mandal"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print(f"📂 Folder created: {folder_name}")

# ---------------------------
# 2. Database path inside your folder
# ---------------------------
db_file = os.path.join(folder_name, "crypto.db")

if os.path.exists(db_file):
    os.remove(db_file)
    print("🗑️ Old database deleted. Creating new one...")

# ---------------------------
# 3. Database connection
# ---------------------------
conn = sqlite3.connect(db_file)

# ---------------------------
# 4. Function: Save data
# ---------------------------
def save_to_db(df, table_name):
    df.to_sql(table_name, conn, if_exists="replace", index=False)  # overwrite
    print(f"✅ Data saved to table: {table_name}")

# ---------------------------
# 5. Download crypto data
# ---------------------------
cryptos = ["BTC-USD", "ETH-USD"]
start = "2023-01-01"
end = "2023-12-31"

for symbol in cryptos:
    data = yf.download(symbol, start=start, end=end)
    data.reset_index(inplace=True)

    # Fix columns → flatten MultiIndex (in case yfinance returns tuple cols)
    data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]

    save_to_db(data, symbol.replace("-", "_"))  # e.g., BTC_USD

# ---------------------------
# 6. Calculate Metrics
# ---------------------------
metrics = []

for symbol in cryptos:
    df = pd.read_sql(f"SELECT * FROM {symbol.replace('-', '_')}", conn)

    mean_close = df["Close"].mean()
    min_close = df["Close"].min()
    max_close = df["Close"].max()
    volatility = df["Close"].std()

    metrics.append({
        "Crypto": symbol,
        "Mean Close": mean_close,
        "Min Close": min_close,
        "Max Close": max_close,
        "Volatility": volatility
    })

metrics_df = pd.DataFrame(metrics)

# ---------------------------
# 7. Save metrics table
# ---------------------------
save_to_db(metrics_df, "metrics")

# ---------------------------
# 8. Show Metrics
# ---------------------------
print("\n📊 Metrics DataFrame:")
print(metrics_df)

# Close DB connection
conn.close()
