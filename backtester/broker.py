class Broker:
    def __init__(self, cash: float = 1_000_000):
        self.cash = cash
        self.position = 0

    def market_order(self, side: str, qty: int, price: float):
        if side not in {"BUY", "SELL"}:
            raise ValueError("Invalid order side")
        if qty <= 0:
            raise ValueError("Quantity must be positive")
        if price <= 0:
            raise ValueError("Price must be positive")
        
        if side == "BUY":
            if self.cash >= qty * price:
                self.position += qty
                self.cash -= qty * price
            else:
                raise ValueError("Not enough cash")

        elif side == "SELL":
            if self.position >= qty:
                self.position -= qty
                self.cash += qty * price
            else:
                raise ValueError("Not enough shares")
            