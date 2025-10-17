import pandas as pd
from backtester.strategy import VolatilityBreakoutStrategy

def test_signals_basic_shape():
    idx = pd.date_range("2025-01-01", periods=5, freq="D") # build a tiny, deterministic price series (5 days)
    prices = pd.Series([100, 101, 102, 103, 104], index=idx)
    strat = VolatilityBreakoutStrategy(window=3)
    sig = strat.signals(prices)
    # Assert: verify basic truths about the result (no math, just structure).
    # "Assert" means: check that what we got matches what we expect.

    assert isinstance(sig, pd.Series) # Check if the function returns a pandas Series
    assert len(sig) == len(prices) # Check if the length of the input and the series is the same
    assert (sig.index == prices.index).all() # Check if the dates for the signals match with the dates of the input


def test_signals_are_binary():
    
    idx = pd.date_range("2025-01-01", periods=6, freq="D")
    prices = pd.Series([100, 102, 101, 103, 102, 104], index=idx)
    strat = VolatilityBreakoutStrategy(window=3)

    sig = strat.signals(prices)

    uniques = set(sig.unique())
    assert uniques.issubset({0, 1})


def test_empty_series_returns_empty():
    # Arrange: empty Series (correct dtype)
    prices = pd.Series(dtype=float)
    strat = VolatilityBreakoutStrategy(window=3)
    sig = strat.signals(prices)

    assert isinstance(sig, pd.Series)
    assert len(sig) == 0

def test_short_series_smaller_than_window():
    """Strategy should handle series shorter than rolling window."""
    # Arrange: only 3 prices, but window = 20
    idx = pd.date_range("2025-01-01", periods=3, freq="D")
    prices = pd.Series([100, 101, 102], index=idx)
    strat = VolatilityBreakoutStrategy()

    sig = strat.signals(prices)

    assert isinstance(sig, pd.Series)
    assert len(sig) == len(prices)
    assert not sig.isna().any()   # no NaNs (since you .fillna(0))
    assert (sig == 0).all()   # all zeros — because breakout not possible with so few points


def test_head_nans_become_zeros():
    """If early prices are NaN, output signals there should be 0 (not NaN)."""
    idx = pd.date_range("2025-01-01", periods=6, freq="D")
    prices = pd.Series([float('nan'), float('nan'), 100, 101, 102, 103], index=idx)

    strat = VolatilityBreakoutStrategy(window=3)
    sig = strat.signals(prices)
    print(sig)

    # same length and index
    assert len(sig) == len(prices)
    assert (sig.index == prices.index).all()

    # no NaNs in signals
    assert not sig.isna().any()

    # the first two (where input was NaN) must produce 0 signals
    assert sig.iloc[0] == 0
    assert sig.iloc[1] == 0

    # the rest must still be binary
    assert set(sig.iloc[2:].unique()).issubset({0, 1})
