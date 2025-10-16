class Broker:
    def __init__(self, cash: float = 1_000_000):
        self.cash = cash
        self.position = 0

    def market_order(self, side: str, qty: int, price: float):
        if side == 'BUY':
            if  self.cash >= qty * price:
                self.position += qty
                self.cash -= qty * price
        elif side == 'SELL':
            if self.position >= qty:
                self.position -= qty
                self.cash += qty * price
        else:
            print('fucking do your shit')
            