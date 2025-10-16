import pandas as pd

def apply_shock(combined_df, shock_date, shock_map):
    df = combined_df.copy()
    df["date"] = pd.to_datetime(df["date"])
    shocked = df.copy()
    for asset, shock in shock_map.items():
        mask = (shocked["asset"]==asset) & (shocked["date"]>=pd.to_datetime(shock_date))
        shocked.loc[mask,"close"] *= (1+shock)
    return shocked
