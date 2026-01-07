# European Option Pricing App

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
