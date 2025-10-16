import sqlite3, pandas as pd
DB_PATH = "results/portfolio_returns.db"

def save_portfolio_returns(df, table_name="portfolio_returns"):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql(table_name, conn, if_exists="replace", index=True)
    conn.close()
