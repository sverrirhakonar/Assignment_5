import pandas as pd
import numpy as np

class VolatilityBreakoutStrategy:
    def __init__(self, window: int = 20):
        self.window = window

    def signals(self, prices: pd.Series) -> pd.Series:

        rets = prices.pct_change()
        vol = rets.rolling(window = self.window).std()

        signal = (rets > vol).astype(int).fillna(0)
        signal.index = prices.index
        return signal
