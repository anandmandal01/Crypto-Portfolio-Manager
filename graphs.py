import pandas as pd
import matplotlib.pyplot as plt
from rules import get_weights_risk_parity
from portfolio import Portfolio

# Load combined CSV
df = pd.read_csv("data/Crypto_metrics_daily.csv", parse_dates=["date"])
assets = sorted(df["asset"].unique())

# Get weights from Risk-Parity
weights = get_weights_risk_parity(assets, df, window=90)
print("Risk-Parity Weights:", weights)

# Portfolio returns
p = Portfolio(df)
port_ret = p.run(weights)

# Cumulative portfolio value
cumulative = (1 + port_ret).cumprod()

# Plot 1: Portfolio Cumulative Returns
plt.figure(figsize=(10,5))
plt.plot(cumulative.index, cumulative["portfolio_return"], label="Portfolio Value")
plt.title("Portfolio Cumulative Returns (Risk-Parity)")
plt.xlabel("Date")
plt.ylabel("Portfolio Value")
plt.legend()
plt.grid(True)
plt.savefig("results/portfolio_cumulative.png")
plt.show()

# Plot 2: Risk-Parity Weights (bar chart)
plt.figure(figsize=(8,5))
plt.bar(weights.keys(), weights.values())
plt.title("Risk-Parity Weights Allocation")
plt.ylabel("Weight")
plt.grid(axis="y")
plt.savefig("results/portfolio_weights.png")
plt.show()

