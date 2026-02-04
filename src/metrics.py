import numpy as np
import pandas as pd

def compute_metrics(equality_curve):
    df = pd.DataFrame(equality_curve).copy()
    df = df.sort_values("dt").reset_index(drop = True)
    df["returns"] = df ["equity"].pct_change().fillna(0.0)

    total_return = (df["equity"].iloc[-1]/df["equity"].iloc[0]) - 1.0

    running_max = df["equity"].cummax()
    drawdown = (df["equity"]/running_max) - 1.0
    max_drawdown = drawdown.min()

    r = df["returns"].values
    if np.std(r) > 0:
        sharpe = np.sqrt(252) * np.mean(r) / np.std(r)
    else:
        sharpe = 0.0

    return {
        "total_return" : float(total_return),
        "max_drawdown" : float(max_drawdown),
        "sharpe" : float(sharpe),
        "equity_df" :df,
    }