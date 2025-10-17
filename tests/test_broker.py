import pytest


def test_buy_updates_cash_and_pos(broker):
    broker.market_order("BUY", 2, 200)
    assert broker.cash == 1000 - 400
    assert broker.position == 2

def test_sell_updates_cash_and_pos(broker):
    # setup: own 2 shares
    broker.market_order("BUY", 2, 200)
    assert (broker.cash, broker.position) == (600, 2)

    # act: sell 1 at 150
    broker.market_order("SELL", 1, 150)
    assert broker.cash == 600 + 150   # 750
    assert broker.position == 1

def test_rejects_invalid_side(broker):
    with pytest.raises(ValueError):
        broker.market_order("HOLD", 1, 100)

def test_rejects_nonpositive_qty(broker):
    # qty <= 0 should raise for both sides
    with pytest.raises(ValueError):
        broker.market_order("BUY", 0, 100)
    with pytest.raises(ValueError):
        broker.market_order("SELL", -1, 100)

def test_rejects_nonpositive_price(broker):
    # price <= 0 should raise for both sides
    with pytest.raises(ValueError):
        broker.market_order("BUY", 1, 0)
    with pytest.raises(ValueError):
        broker.market_order("SELL", 1, -50)

def test_rejects_insufficient_cash(broker):
    # can’t afford 1 share at 1500 with $1000
    with pytest.raises(ValueError):
        broker.market_order("BUY", 1, 1500)


def test_rejects_insufficient_shares(broker):
    broker.market_order("BUY", 1, 50)  # own 1
    with pytest.raises(ValueError):
        broker.market_order("SELL", 3, 50)  # try to oversell
