import pandas as pd
import matplotlib.pyplot as plt
from portfolio_math import load_prices, returns_from_prices
import os

def compare_portfolio_vs_asset(prices_path, portfolio_weights, out_dir='outputs'):
    os.makedirs(out_dir, exist_ok=True)
    prices = load_prices(prices_path)
    returns = returns_from_prices(prices)
    # compute cumulative returns (assume daily compounding)
    port_daily = (returns * portfolio_weights).sum(axis=1)
    port_cum = (1 + port_daily).cumprod() - 1
    # choose single asset (e.g., DOGE) for comparison
    single = returns['DOGE'].cumprod() - 1
    df = pd.DataFrame({'portfolio_cum': port_cum, 'doge_cum': single})
    csv_path = os.path.join(out_dir, 'comparison.csv')
    df.to_csv(csv_path, index=True)
    # plot
    plt.figure(figsize=(8,4))
    plt.plot(df.index, df['portfolio_cum'], label='Portfolio (example)')
    plt.plot(df.index, df['doge_cum'], label='DOGE (single asset)')
    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.title('Portfolio vs DOGE')
    img_path = os.path.join(out_dir, 'comparison.png')
    plt.tight_layout()
    plt.savefig(img_path)
    plt.close()
    return {'csv': csv_path, 'plot': img_path}
