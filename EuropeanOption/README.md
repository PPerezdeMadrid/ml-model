# European Option Pricing App

Based on https://github.com/just-krivi/option-pricing-models
## Description

This project aims to calculate a European option price. 
A European option is a financial derivative that **can only be exercised on its expiration date**, not before.

Example:
Suppose you buy a European call option on a stock with a **strike price of $100** and an **expiration date of June 30**.

* If the stock price is above $100 on June 30, you can exercise the option and buy the stock at $100.
* If the stock price is below $100 on June 30, the option expires worthless.

You cannot exercise the option before June 30, regardless of how high the stock price goes earlier.

## Objectives

- Implement and understand the theoretical foundations of European option pricing.
- Price European call and put options using three different approaches:
  - Black–Scholes model
  - Monte Carlo simulation
  - Binomial tree model
- Compare the results obtained by each method and analyze their convergence and accuracy.
- Study the impact of key parameters (volatility, time to maturity, interest rate) on option prices.
- Validate numerical methods by benchmarking them against the Black–Scholes model.

## App Overview
App to price European call/put options with Black-Scholes using historical volatility from Yahoo Finance. Includes a Streamlit UI and a small CLI example.

![Streamlit demo](europeanOption.gif)

## Key files
- `streamlit_app.py`: Streamlit UI, downloads prices with yfinance, computes rolling sigma, plots the series, and prices with Black-Scholes.
- `data.py`: utilities to fetch spot price and historical volatility.
- `model/blackscholes.py`: minimal Black-Scholes implementation.
- `europeanOption.py`: quick CLI example.

## Requirements
- Python 3.10+ recommended.
- Dependencies in `../requirements.txt` (numpy, pandas, matplotlib, yfinance, streamlit...).
- Internet connection for yfinance downloads.

### Quick setup
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r ../requirements.txt
```

## How to run

### Streamlit app
From `EuropeanOption/`:
```bash
streamlit run streamlit_app.py
```
- Streamlit will launch at `http://localhost:8501`. If it does not open automatically, copy the URL into your browser.
- Sidebar parameters:
  - `Method`: only Black-Scholes is implemented (Monte Carlo and Binomial are placeholders).
  - `Market data`: ticker (e.g., AAPL), history period, and whether to use Adj Close.
  - `Rolling window / trading days`: control the annualized historical sigma.
  - `Option inputs`: type (call/put), strike K, maturity in days T, risk-free rate r, dividend yield q.
  - `Sigma choice`: latest rolling sigma, pick a date in the series, or enter a manual sigma.
- Click **Calculate**. The app downloads prices, computes rolling volatility, plots the series, and shows the Black-Scholes price with the inputs used.
- If the rolling series is empty, try a longer period or a smaller window.
- Running from another folder? Use the absolute path:  
  `streamlit run "/Users/palomaperezdemadrid/Desktop/Data Scientist/ml-model/EuropeanOption/streamlit_app.py"`

## Notes
- yfinance may be slow or rate-limited for some tickers; change the ticker or retry if it happens.
- Volatility uses daily log returns and annualizes with 252 trading days.
- Paths above assume you execute commands inside `EuropeanOption/`. Adjust if you run from elsewhere.
