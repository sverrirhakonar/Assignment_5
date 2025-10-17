# tests/test_engine.py
import pandas as pd
from unittest.mock import MagicMock

from backtester.engine import Backtester

def test_engine_trades_at_t_using_signal_from_t_minus_1(broker):
    # Arrange: 5 days of prices
    idx = pd.date_range("2025-01-01", periods=5, freq="D")
    prices = pd.Series([100.0, 101.0, 102.0, 103.0, 104.0], index=idx)

    # Fake strategy: signals are 0, then from index 2 onward they are 1.
    # Engine uses signals.shift(1), so:
    #  - at t=2: action uses signal[t-1]=0 -> no trade
    #  - at t=3: action uses signal[t-1]=1 -> BUY at price[t=3]
    fake_strategy = MagicMock()
    fake_signals = pd.Series(0, index=idx)
    fake_signals.iloc[2:] = 1
    fake_strategy.signals.return_value = fake_signals

    # Build engine but bypass default ctor (which would instantiate real classes)
    bt = Backtester(strategy=lambda: None, broker=lambda: None)
    bt.strategy = fake_strategy
    bt.broker = broker  # fresh broker from fixture (cash=1000)

    # Act
    equity = bt.run(prices)

    # Assert (timing checks)
    # At t=2 (no trade yet)
    assert equity.loc[idx[2], "position"] == 0
    assert equity.loc[idx[2], "cash"] == 1000

    # At t=3 (BUY 1 at price[3])
    assert equity.loc[idx[3], "position"] == 1
    assert equity.loc[idx[3], "cash"] == 1000 - prices.loc[idx[3]]

    # Final broker state remains long
    assert broker.position == 1
    assert broker.cash == 1000 - prices.iloc[3]


def test_equity_matches_cash_plus_position_times_price(broker):
    # Arrange: simple prices
    idx = pd.date_range("2025-01-01", periods=6, freq="D")
    prices = pd.Series([100.0, 101.0, 102.0, 103.0, 104.0, 105.0], index=idx)

    # Fake strategy: some buys/sells after shift(1)
    fake_strategy = MagicMock()
    fake_strategy.signals.return_value = pd.Series([0, 1, 1, 0, 0, 1], index=idx)

    bt = Backtester(strategy=lambda: None, broker=lambda: None)
    bt.strategy = fake_strategy
    bt.broker = broker

    # Act
    equity_df = bt.run(prices)

    # Assert: equity == cash + position * price (elementwise)
    computed = equity_df["cash"] + equity_df["position"] * prices
    pd.testing.assert_series_equal(
        equity_df["equity"].astype(float),
        computed.astype(float),
        check_names=False,
        atol=1e-9,
        rtol=1e-9,
        check_exact=False,
    )


def test_end_to_end_tiny_scenario_final_state(broker):
    # Prices across 5 days
    idx = pd.date_range("2025-01-01", periods=5, freq="D")
    prices = pd.Series([100.0, 102.0, 101.0, 105.0, 104.0], index=idx)

    # Fake strategy (unshifted). Engine will use shift(1) internally.
    # signals = [0, 1, 1, 0, 0]  -> actions after shift = [0, 0, 1, 1, 0]
    fake_strategy = MagicMock()
    fake_strategy.signals.return_value = pd.Series([0, 1, 1, 0, 0], index=idx)

    bt = Backtester(strategy=lambda: None, broker=lambda: None)
    bt.strategy = fake_strategy
    bt.broker = broker  # $1000 starting cash

    # Act
    equity_df = bt.run(prices)

    # Assert final state (hand-calculated): cash 1003, pos 0, equity 1003
    last = equity_df.iloc[-1]
    assert last["cash"] == 1003.0
    assert last["position"] == 0
    assert last["equity"] == 1003.0
