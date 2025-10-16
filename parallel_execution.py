from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime
from portfolio_math import load_prices, returns_from_prices, equal_weights, rule_based_weights, portfolio_return, portfolio_volatility
from db_portfolio import init_db, store_portfolio
import pandas as pd

def run_strategy(name, prices_path):
    prices = load_prices(prices_path)
    returns = returns_from_prices(prices)
    mean_returns = returns.mean()  # average daily
    cov = returns.cov()  # daily covariance

    if name == 'equal':
        weights = equal_weights(returns.columns)
    elif name == 'rule':
        weights = rule_based_weights(returns.columns)
    else:
        # default to equal
        weights = equal_weights(returns.columns)

    total_ret = portfolio_return(weights, mean_returns)
    vol = portfolio_volatility(weights, cov)

    assets_meta = {}
    for a in returns.columns:
        assets_meta[a] = {
            'weight': float(weights[a]),
            'mean_return': float(mean_returns[a]),
            'variance': float(returns[a].var())
        }

    # store into DB
    init_db()
    store_portfolio(name, datetime.datetime.utcnow().isoformat(), float(total_ret), float(vol), assets_meta)

    return {'name': name, 'total_return': total_ret, 'volatility': vol, 'weights': weights}

def run_all(prices_path):
    strategies = ['equal', 'rule', 'performance']
    results = []
    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = {ex.submit(run_strategy, s, prices_path): s for s in strategies}
        for fut in as_completed(futures):
            res = fut.result()
            results.append(res)
    return results
