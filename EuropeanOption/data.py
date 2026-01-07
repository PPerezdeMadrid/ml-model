import yfinance as yf
import numpy as np


def get_spot_price(ticker: str) -> float:
    """
    Fetch the latest available spot price from Yahoo Finance.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")

    if data.empty:
        raise ValueError(f"No data returned for ticker {ticker}")

    # Use the last close price
    spot_price = data["Close"].iloc[-1]
    return float(spot_price)

def get_hist_vol_annualized(ticker, period="1y", use_adj_close = True, trading_days=252):
    """
    Annualized historical volatility (sigma) from daily log returns.
    period examples: "6mo", "1y", "2y", "5y"
    """
    df = yf.download(ticker, period=period, interval="1d", auto_adjust=False)
    if df.empty:
        raise ValueError(f"No price data for ticker {ticker}")

    if use_adj_close and "Adj Close" in df.columns:
        price_col = "Adj Close"
    else:
        price_col = "Close"

    prices = df[price_col].dropna()

    # Daily log returns
    log_returns = np.log(prices/prices.shift(1)).dropna()

    # Annualized sigma
    sigma = log_returns.std(ddof=1) * np.sqrt(trading_days)
    # return float(sigma)
    return float(sigma.iloc[0])

def rolling_hist_vol(ticker, period="1y", use_adj_close = True, trading_days=252, window=30):
    df=yf.download(ticker, period=period, interval="1d", auto_adjust=False, progress=False)
    if df.empty:
        raise ValueError(f"No price data for ticker {ticker}")
    
    if use_adj_close and "Adj Close" in df.columns:
        price_col = "Adj Close"
    else:
        price_col = "Close"
    prices = df[price_col].dropna()

    log_returns = np.log(prices/prices.shift(1)).dropna()
    rolling_sigma = log_returns.rolling(window).std(ddof=1) * np.sqrt(trading_days)
    rolling_sigma.name = f"{window}D_rolling_sigma"

    return rolling_sigma    
    # return rolling_sigma.dropna().iloc[-1].item()