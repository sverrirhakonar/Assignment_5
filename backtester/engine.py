import pandas as pd
from broker import Broker
from strategy import VolatilityBreakoutStrategy
from price_loader import load_market_data

class Backtester:
    def __init__(self, strategy = VolatilityBreakoutStrategy(), broker = Broker()):
        self.strategy = strategy
        self.broker = broker

    def run(self, prices: pd.Series):
        signals = self.strategy.signals(prices)

        for t in range(1, len(prices)):
            signal = signals[t-1]
            price = prices[t]
            if signal == 1:
                self.broker.market_order('BUY', 1, price)
            elif signal == 0:
                self.broker.market_order('SELL', 1, price)



p = load_market_data('market_data.csv')
b = Backtester()
b.run(p.price)