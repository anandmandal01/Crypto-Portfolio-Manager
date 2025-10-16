from parallel_execution import run_all
from portfolio_math import load_prices, returns_from_prices, rule_based_weights
from portfolio_comparison import compare_portfolio_vs_asset
import pprint, os

DATA_PATH = 'sample_prices.csv'

def main():
    print('Running Milestone 2 project end-to-end...')
    results = run_all(DATA_PATH)
    pprint.pprint(results)

    # For presentation: compute a rule-based example weights and compare
    prices = load_prices(DATA_PATH)
    returns = returns_from_prices(prices)
    weights = rule_based_weights(returns.columns)
    out = compare_portfolio_vs_asset(DATA_PATH, weights)
    print('\nComparison outputs:')
    pprint.pprint(out)
    print('\nOutputs saved in outputs/ folder and DB milestone2_portfolio.db')

if __name__ == '__main__':
    main()
