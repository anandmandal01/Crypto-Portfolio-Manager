import numpy as np
import pandas as pd

def load_prices(path):
    df = pd.read_csv(path, parse_dates=['date']).set_index('date').sort_index()
    return df

def returns_from_prices(prices_df):
    # daily simple returns
    returns = prices_df.pct_change().dropna()
    return returns

def rule_based_weights(assets):
    # Example rule: safer coins get higher weights
    # We'll define a priority mapping: BTC and USDT high, ETH medium, others low.
    priority = {
        'BTC': 3,
        'USDT': 3,
        'ETH': 2,
        'AAVE': 1,
        'UNI': 1,
        'DOGE': 0.5
    }
    w = np.array([priority.get(a,1) for a in assets], dtype=float)
    w = w / w.sum()
    return pd.Series(w, index=assets)

def equal_weights(assets):
    n = len(assets)
    return pd.Series(np.repeat(1.0/n, n), index=assets)

def portfolio_return(weights, mean_returns):
    # weights: pd.Series, mean_returns: pd.Series (periodic)
    return (weights * mean_returns).sum()

def portfolio_volatility(weights, cov_matrix):
    w = weights.values.reshape(-1,1)
    var = float(w.T @ cov_matrix.values @ w)
    return np.sqrt(var)
