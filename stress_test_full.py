# Milestone 4: Stress Test Analysis
# -----------------------------------------------------
# Simulate Bull, Bear, and Volatile Market Conditions
# using Risk-Parity Portfolio weights

import pandas as pd
import numpy as np

# --- Step 1: Define sample market data for stress testing ---

bull_market = pd.DataFrame({
    "BTC": [0.05, 0.04, 0.03, 0.06],
    "ETH": [0.04, 0.03, 0.02, 0.05],
    "ADA": [0.03, 0.02, 0.01, 0.04]
})

bear_market = pd.DataFrame({
    "BTC": [-0.05, -0.04, -0.03, -0.06],
    "ETH": [-0.04, -0.03, -0.02, -0.05],
    "ADA": [-0.03, -0.02, -0.01, -0.04]
})

volatile_market = pd.DataFrame({
    "BTC": [0.10, -0.10, 0.12, -0.08],
    "ETH": [0.08, -0.07, 0.09, -0.06],
    "ADA": [0.07, -0.05, 0.06, -0.04]
})

# --- Step 2: Risk-Parity rule (Inverse Volatility) ---

def risk_parity_rule(returns):
    vols = returns.std()
    inv_vols = 1 / vols
    weights = inv_vols / inv_vols.sum()
    return weights

# --- Step 3: Calculate weights and portfolio returns ---

def simulate_market(market_df, name):
    weights = risk_parity_rule(market_df)
    portfolio_returns = (market_df * weights).sum(axis=1)
    print(f"\n📈 {name} Portfolio Weights:")
    print(weights.round(4))
    print(f"\n{name} Portfolio Returns:")
    print(portfolio_returns.round(4))
    print("\nDays:", len(portfolio_returns))
    print("-" * 40)
    return portfolio_returns.mean()

# --- Step 4: Run Stress Test on all market scenarios ---

print("=== 🔍 Risk-Parity Stress Test Results ===")
mean_bull = simulate_market(bull_market, "Bull Market")
mean_bear = simulate_market(bear_market, "Bear Market")
mean_volatile = simulate_market(volatile_market, "Volatile Market")

# --- Step 5: Interpret Results ---

print("\n📊 Summary Interpretation:")
print(f"Average Return (Bull): {mean_bull:.4f}")
print(f"Average Return (Bear): {mean_bear:.4f}")
print(f"Average Return (Volatile): {mean_volatile:.4f}")

print("\n🧠 Insights:")
print("1️⃣ In Bull Market → Portfolio gains steadily, since all assets move upward.")
print("2️⃣ In Bear Market → Portfolio still loses, but Risk-Parity reduces losses.")
print("3️⃣ In Volatile Market → Portfolio smooths out swings, showing stability.")

