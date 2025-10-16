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
        equity_curve = [] # will include [cash, posistion, total value at each instance]
        for t in range(1, len(prices)):
            signal = signals.iloc[t-1]
            price = prices.iloc[t]
            if signal == 1:
                if self.broker.position == 0:
                    self.broker.market_order('BUY', 1, price)
            elif signal == 0:
                if self.broker.position != 0:
                    self.broker.market_order('SELL', 1, price)
            equity_curve.append([[self.broker.cash, self.broker.position, self.broker.cash + self.broker.position * price]])
        return equity_curve



p = load_market_data('market_data.csv')
b = Backtester()
c = b.run(p.price)
print(c)