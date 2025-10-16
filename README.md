# 🚀 Crypto Portfolio Manager  

### 🧑‍💻 Author: **Anand Kumar Mandal**  
**Guide:** Prof. Rajalakshmi  
📧 Email: anandkumarmandal708@gmail.com  

---

## 📘 Project Overview
**Crypto Portfolio Manager** is a Python-based project that automates cryptocurrency portfolio tracking, risk analysis, stress testing, and performance prediction.  
It combines **finance analytics + AI predictions** to evaluate the stability and efficiency of crypto portfolios under varying market conditions.

---

## 🧩 Milestone Summary

### **Milestone 1 – Data Collection**
- Downloads cryptocurrency data (BTC, ETH, USDT) from Binance/YFinance.  
- Computes daily metrics: Mean, Min, Max, and Volatility.  
- Stores data securely in a SQLite database.

---

### **Milestone 2 – Portfolio Management**
- Builds **Equal-weight** and **Rule-based** portfolios.  
- Calculates overall **returns, volatility, and cumulative growth**.  
- Visualizes results and compares portfolio vs. single asset.

---

### **Milestone 3 – Database & Metrics**
- Stores metrics, volatility, and portfolio results in a database.  
- Generates performance CSVs for daily and cumulative returns.  
- Establishes database structure for predictions and alerts.

---

### **Milestone 4 – Risk Analysis, Stress Testing & ML Prediction**
- Applies **Risk Rules**:
  - Volatility threshold checks  
  - Sharpe Ratio  
  - Sortino Ratio  
  - Maximum Drawdown  
  - Maximum Asset Weight
- Implements **Stress Testing** to simulate market shocks and portfolio resilience.
- Sends **Email & AI Alerts** when thresholds are breached.  
- Integrates **Machine Learning (Linear Regression)** for future return prediction.  
- Stores predictions and performance metrics in database.

---

## ⚙️ Features
| Category | Description |
|-----------|--------------|
| 📊 Data Handling | Automated crypto data collection and cleaning |
| 💾 Database | SQLite-based persistent storage for metrics & alerts |
| ⚖️ Risk Analysis | Real-time Sharpe, Sortino, Volatility, Max Drawdown |
| 🧠 Machine Learning | Linear Regression model for asset & portfolio prediction |
| 📈 Stress Testing | Portfolio stability under extreme market conditions |
| 📧 Alerts | Automatic email + AI alerts for failed risk rules |
| 📂 Outputs | CSV and image-based visual reports |

---

## 🧮 Methodology
1. **Data Preprocessing** – Fetch data from Binance or CSVs.  
2. **Portfolio Building** – Construct using rule-based & equal-weight methods.  
3. **Risk Computation** – Calculate key performance ratios.  
4. **Stress Testing** – Simulate negative shocks and re-evaluate portfolio.  
5. **Prediction** – Train Linear Regression for next-step forecasts.  
6. **Alert System** – Store and email alerts for risky conditions.

---

🧰 Tools & Libraries

Language: Python 3.10+

Libraries: Pandas, NumPy, Matplotlib, scikit-learn, SQLite3, smtplib, yfinance

Environment: Visual Studio Code

🧾 Files Overview
File	Description
milestone1_crypto.py	Downloads crypto data & saves to DB
db_portfolio.py	Handles portfolio database functions
Risk_checker.py	Applies risk rules & triggers alerts
stress_test.py / stress_test_full.py	Performs portfolio stress testing
predictor.py	ML module using Linear Regression
mailSending.py	Sends email alerts & logs AI notifications
portfolio_math.py	Financial formulas for Sharpe, Sortino, etc.
main.py	Integrates all modules and runs full analysis
README.md	Project documentation
LICENSE	MIT License
/AgileDocs/	Agile documentation (Backlog, Review, Retrospective)

🧱 Project Folder Structure
📁 Crypto-Portfolio-Manager
│
├── milestone1_crypto.py
├── db_portfolio.py
├── mailSending.py
├── portfolio_math.py
├── Risk_checker.py
├── stress_test.py
├── stress_test_full.py
├── predictor.py
├── main.py
│
├── 📂 Data/
│   ├── Binance_BTCUSDT_d.csv
│   ├── Binance_ETHUSDT_d.csv
│   ├── Binance_USDCUSDT_d.csv
│
├── 📂 AgileDocs/
│   ├── Project_Backlog.md
│   ├── Sprint_Review.md
│   └── Retrospective.md
│
└── 📂 Outputs/
    ├── comparison.csv
    ├── comparison.png
