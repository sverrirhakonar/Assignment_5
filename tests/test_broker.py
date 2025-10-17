import pytest
import pandas as pd
from backtester.broker import Broker

def test_if_buy_updated_cash_and_pos():
    """ Test that buying reduces cash and increases position correctly."""
    some_broker = Broker(cash= 1000)
    some_broker.market_order('BUY', 2, 200)

    assert some_broker.cash == 600
    assert some_broker.position == 2

def test_if_sell_updated_cash_and_pos():
    """ Test that selling reduces cash and increases position correctly."""
    some_broker = Broker(cash= 1000)
    some_broker.market_order('BUY', 2, 200)

    assert some_broker.cash == 600
    assert some_broker.position == 2

    some_broker.market_order('SELL', 1, 150)

    assert some_broker.cash == 750
    assert some_broker.position == 1

def test_rejects_invalid_orders():
    """Broker should raise ValueError for bad inputs."""
    broker = Broker(cash=1000)
    with pytest.raises(ValueError): # Hold is not a signal so error
        broker.market_order("HOLD", 1, 100)

    with pytest.raises(ValueError): # buy 0 shares? so error
        broker.market_order("BUY", 0, 100)

    with pytest.raises(ValueError): # sell at a negative price? so error
        broker.market_order("SELL", 1, -50)

def test_rejects_insufficient_cash():
    """Broker should raise ValueError when buying without enough cash."""
    broker = Broker(cash=1000)
    with pytest.raises(ValueError):
        broker.market_order("BUY", 1, 1500)

def test_rejects_insufficient_shares():
    """Broker should raise ValueError when selling more than position."""
    broker = Broker(cash=1000)
    broker.market_order("BUY", 1, 50)  # buy one share
    with pytest.raises(ValueError):
        broker.market_order("SELL", 3, 50)  # try to oversell
