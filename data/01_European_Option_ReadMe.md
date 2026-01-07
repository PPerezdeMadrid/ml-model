# Market Data Notebook

This notebook pulls market inputs from Yahoo Finance with yfinance and prepares volatility metrics for option pricing pipelines.

Contents:
- Setup: install deps via `pip install -r ../requirements.txt`.
- `get_spot_price(ticker)`: fetches the latest close/spot price; example prints an AAPL quote.
- Option inputs: outlines a pipeline using spot, strike, maturity, and a risk-free rate, noting the difference between historical versus implied volatility.
- `get_hist_vol_annualized(ticker, period, use_adj_close=True, trading_days=252)`: downloads daily prices (prefers Adjusted Close), computes daily log returns, and annualizes sigma (example: 1Y AAPL).
- `rolling_hist_vol(ticker, period, use_adj_close=True, trading_days=252, window=30)`: returns a rolling annualized volatility series; NaNs appear during the initial window warm-up; example extracts the latest 30-day value.

Outputs: prints spot price, the full rolling series, and recent historical/rolling volatility figures that can feed Black-Scholes, Monte Carlo, or binomial pricing models.
