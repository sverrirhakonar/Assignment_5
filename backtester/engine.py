import pandas as pd
from broker import Broker
from strategy import VolatilityBreakoutStrategy
from price_loader import load_market_data

class Backtester:
    def __init__(self, strategy = VolatilityBreakoutStrategy, broker = Broker):
        self.strategy = strategy()
        self.broker = broker()


    def run(self, prices: pd.Series):
        signals = self.strategy.signals(prices)
        signals = signals.shift(1).fillna(0).astype(int)

        equity_curve = [] # will include [cash, posistion, total value at each instance]

        for t in range(len(prices)):
            action = signals.iloc[t]
            price = prices.iloc[t]
            if action == 1:
                if self.broker.position == 0:
                    self.broker.market_order('BUY', 1, price)
            elif action == 0:
                if self.broker.position != 0:
                    self.broker.market_order('SELL', self.broker.position, price)
            equity_curve.append([self.broker.cash, self.broker.position, self.broker.cash + self.broker.position * price])
        return pd.DataFrame(equity_curve, columns=["cash", "position", "equity"], index=prices.index)





