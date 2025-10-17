# trading-ci-lab

Minimal daily-bar backtester focused on **testing, coverage, and CI** (not alpha).

## What’s inside
- **PriceLoader** → returns prices as a `pandas.DataFrame` (`timestamp` index, `price` column)
- **VolatilityBreakoutStrategy** → signals 0/1 via rolling std of returns
- **Broker** → simple market-order model (no fees/slippage)
- **Backtester** → end-of-day loop, trades at t using signal[t-1], tracks cash/position/equity

## Run tests locally
```bash
pip install -r requirements.txt
coverage run -m pytest -q
coverage report
# optional:
# coverage html  # open htmlcov/index.html
