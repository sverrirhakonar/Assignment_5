# 📈 Volatility Breakout Backtester

This project implements a minimal but fully tested **backtesting engine** for a simple *volatility breakout* trading strategy.

It includes:
- `VolatilityBreakoutStrategy` – generates trading signals.
- `Broker` – handles cash and positions.
- `Backtester` – runs the strategy over prices.
- `PriceLoader` – reads and formats price data.
- Comprehensive unit tests with >90% coverage.

---

## 🧠 Design Notes

### Strategy

The `VolatilityBreakoutStrategy` computes returns and rolling volatility:

```python
rets = prices.pct_change()
vol = rets.rolling(window).std()
signal = (rets > vol).astype(int).fillna(0)
```

- Signal represents **target position**: 1 = want to own 1 share, 0 = want to own 0 shares
- If signal = 1 and we don't own: BUY 1 share
- If signal = 0 and we own 1 share: SELL 1 share
- Uses a rolling standard deviation window to detect breakouts.
- Handles NaNs safely and always returns a Series matching the price index.

### Broker

The `Broker` class maintains account state:
- `cash`: current balance
- `position`: number of held shares

It executes orders via:

```python
broker.market_order("BUY", qty, price)
broker.market_order("SELL", qty, price)
```

and raises errors for:
- invalid sides (not "BUY" or "SELL")
- insufficient cash or shares
- zero or negative quantities

### Backtester

The `Backtester` integrates strategy and broker:
- Uses signals shifted by one period (to trade at t using signal from t−1).
- Updates equity each step using: **Equity(t) = Cash(t) + Position(t) × Price(t)**
- Returns a DataFrame of cash, position, and equity over time.

### Price Loader

The `PriceLoader` handles reading and cleaning CSV files:
- Parses timestamps
- Casts prices to floats
- Sorts chronologically

---

## ⚙️ How to Run Tests

Install dependencies:

```bash
pip install pytest coverage
```

Run all tests:

```bash
pytest -q
```

Run with coverage:

```bash
coverage run -m pytest -q
coverage report -m
```

Generate HTML coverage report:

```bash
coverage html
start htmlcov/index.html
```

---

## ✅ Continuous Integration (CI)

GitHub Actions runs tests automatically and enforces 90%+ coverage.

Example workflow snippet:

```yaml
- name: Run tests with coverage
  run: |
    coverage run -m pytest -q
    coverage report --fail-under=90
```

### CI Status

![CI passing](docs/github_actions_successful.png)

---

## 📊 Coverage Summary

Example local coverage output:

| File | Coverage |
|------|----------|
| backtester/__init__.py | 100% |
| backtester/broker.py | 100% |
| backtester/engine.py | 100% |
| backtester/strategy.py | 100% |
| **TOTAL** | **100%** |

### 📸 Visual report:

![Coverage Report](docs/coverage_report.png)

---

## 🧪 Tests Overview

| Module | What's Tested |
|--------|---------------|
| Strategy | Signal shape, NaN handling, binary output, constant prices |
| Broker | Position/cash updates, insufficient funds, invalid orders |
| Engine | Signal timing (t−1 logic), equity accounting, end-to-end scenario |
| Edge Cases | Empty input, short series, rolling window handling |
| Validation | Proper error handling with pytest.raises() |

---

## 📂 Project Structure

```
Assignment_5/
├── backtester/
│   ├── __init__.py
│   ├── broker.py
│   ├── engine.py
│   ├── price_loader.py
│   └── strategy.py
├── tests/
│   ├── test_strategy.py
│   ├── test_broker.py
│   ├── test_engine.py
│   └── conftest.py
├── docs/
│   ├── coverage.png
│   └── github_actions.png
├── htmlcov/
│   └── index.html
├── README.md
├── pyproject.toml
└── .gitignore
```

---

## 🚀 Example Run

```bash
python -m backtester.engine
```

This loads `market_data.csv`, runs the backtest, and prints the final equity.

---

## 🧩 Deliverables Checklist

| Deliverable | Status |
|-------------|--------|
| Code for PriceLoader, Strategy, Broker, Backtester | ✅ |
| Comprehensive unit tests | ✅ |
| CI passing with coverage ≥ 90% | ✅ |
| Coverage report (HTML) generated | ✅ |
| README with screenshots and notes | ✅ |

---

## 🏁 Results

- ✅ All tests passing
- ✅ **Coverage: 100%** 🎉
- ✅ CI passing
- ✅ Clean, modular design