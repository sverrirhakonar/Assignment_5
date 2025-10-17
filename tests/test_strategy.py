import pandas as pd
import numpy as np

def test_signals_basic_shape(prices, strategy):
    sig = strategy.signals(prices)

    assert isinstance(sig, pd.Series)
    assert len(sig) == len(prices)
    assert (sig.index == prices.index).all()


def test_signals_are_binary(prices, strategy):
    sig = strategy.signals(prices)
    uniques = set(sig.unique())

    assert uniques.issubset({0, 1})
    # optional: dtype lock
    assert str(sig.dtype).startswith("int")


def test_empty_series_returns_empty(strategy):
    prices = pd.Series(dtype=float)
    sig = strategy.signals(prices)

    assert isinstance(sig, pd.Series)
    assert len(sig) == 0


def test_short_series_smaller_than_window(strategy):
    """Strategy should handle series shorter than rolling window."""
    idx = pd.date_range("2025-01-01", periods=3, freq="D")
    prices = pd.Series([100, 101, 102], index=idx)

    sig = strategy.signals(prices)

    assert isinstance(sig, pd.Series)
    assert len(sig) == len(prices)
    assert not sig.isna().any()
    assert (sig == 0).all()


def test_head_nans_become_zeros(strategy):
    """If early prices are NaN, output signals there should be 0 (not NaN)."""
    idx = pd.date_range("2025-01-01", periods=6, freq="D")
    prices = pd.Series([np.nan, np.nan, 100, 101, 102, 103], index=idx)

    # use a local strategy with a small window (don’t mutate the fixture)
    local_strat = type(strategy)(window=3)
    sig = local_strat.signals(prices)

    assert len(sig) == len(prices)
    assert (sig.index == prices.index).all()
    assert not sig.isna().any()
    assert sig.iloc[0] == 0
    assert sig.iloc[1] == 0
    assert sig.iloc[2] == 0
    assert sig.iloc[3] == 0
    assert set(sig.iloc[2:].unique()).issubset({0, 1})


def test_internal_nans_produce_0_in_the_window(strategy):
    """
    If there is a NaN at t, the signal at t and any t whose rolling window includes that NaN
    should be 0 (rolling stats NaN -> compare -> 0, then filled to 0).
    """
    idx = pd.date_range("2025-01-01", periods=7, freq="D")
    prices = pd.Series([1, 100, np.nan, 102, 103, 101, 107], index=idx)

    local_strat = type(strategy)(window=3)
    sig = local_strat.signals(prices)

    assert (sig.iloc[2:6] == 0).all()
    assert set(sig.unique()).issubset({0, 1})


def test_const_price_returns_all_zeros(strategy):
    """Flat prices -> returns=0, rolling std=0/NaN -> signals should be all zeros."""
    idx = pd.date_range("2025-01-01", periods=6, freq="D")
    prices = pd.Series([100, 100, 100, 100, 100, 100], index=idx)

    local_strat = type(strategy)(window=4)
    sig = local_strat.signals(prices)

    assert (sig == 0).all()
