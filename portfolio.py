import pandas as pd

class Portfolio:
    def __init__(self, combined_df):
        self.df = combined_df.copy()
        self.df["date"] = pd.to_datetime(self.df["date"])
        self.close_pivot = self.df.pivot(index="date", columns="asset", values="close").sort_index()
        self.returns = self.close_pivot.pct_change().dropna()

    def run(self, weights):
        w_series = pd.Series({a: weights.get(a,0) for a in self.close_pivot.columns})
        port_ret = (self.returns * w_series).sum(axis=1).to_frame(name="portfolio_return")
        return port_ret
