import sqlite3
import pandas as pd
from typing import Dict

DB_PATH = 'milestone2_portfolio.db'

def init_db(path=DB_PATH):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS portfolio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            date_run TEXT,
            total_return REAL,
            volatility REAL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS portfolio_assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            portfolio_id INTEGER,
            asset TEXT,
            weight REAL,
            mean_return REAL,
            variance REAL,
            FOREIGN KEY(portfolio_id) REFERENCES portfolio(id)
        )
    ''')
    conn.commit()
    conn.close()

def store_portfolio(name: str, date_run: str, total_return: float, volatility: float, assets: Dict, db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO portfolio (name, date_run, total_return, volatility) VALUES (?, ?, ?, ?)', 
              (name, date_run, total_return, volatility))
    pid = c.lastrowid
    for asset, meta in assets.items():
        c.execute('INSERT INTO portfolio_assets (portfolio_id, asset, weight, mean_return, variance) VALUES (?, ?, ?, ?, ?)',
                  (pid, asset, meta.get('weight'), meta.get('mean_return'), meta.get('variance')))
    conn.commit()
    conn.close()

def fetch_portfolios(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query('SELECT * FROM portfolio', conn)
    conn.close()
    return df
