import pandas as pd

def get_weights_risk_parity(assets, price_df, window=90):
    vol = {}
    for a in assets:
        s = price_df[price_df["asset"]==a].sort_values("date")["close"].pct_change().dropna()
        vol[a] = s[-window:].std() if len(s) >= window else (s.std() if len(s)>0 else 0)
    inv_vol = {a:(1/vol[a] if vol[a]>0 else 0) for a in assets}
    total = sum(inv_vol.values())
    if total==0: return {a:1/len(assets) for a in assets}
    return {a: inv_vol[a]/total for a in assets}
