# Crypto Portfolio Project - Milestone 2
Author: Anand Kumar Mandal

This is a small runnable project meant for demonstration and presentation in VS Code.
It includes:
- portfolio_math.py  - weight rules, returns, volatility calculations
- db_portfolio.py    - simple SQLite storage for portfolio runs
- parallel_execution.py - run multiple strategies in parallel and store results
- portfolio_comparison.py - compare portfolio vs single asset, export CSV and PNG
- main.py            - run end-to-end example
- sample_prices.csv  - sample price data to run the project

How to run:
1. Create a virtual environment and install requirements:
   ```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   pip install pandas numpy matplotlib python-dateutil
   ```
2. Run in VS Code terminal:
   ```bash
   python main.py
   ```
3. Check outputs/ folder for comparison.csv and comparison.png, and milestone2_portfolio.db for DB results.

Notes:
- The sample_prices.csv contains dummy data for August 2025.
- Adjust weights and strategies as needed for your assignment requirements.
