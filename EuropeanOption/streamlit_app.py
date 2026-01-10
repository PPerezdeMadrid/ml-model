import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

from model.blackscholes import BlackScholes
from model.montecarlo import montecarlo_simulation_european_option
from model.binomialtree import binomial_tree_option_price
from data import rolling_hist_vol
from option_worthiness import assess_worthiness


def get_spot_price(ticker: str) -> float:
    df = yf.download(ticker, period="7d", interval="1d", auto_adjust=False, progress=False)
    if df.empty:
        raise ValueError(f"No data for ticker: {ticker}")
    return float(df["Close"].dropna().iloc[-1])


st.set_page_config(page_title="Option Pricer", layout="centered")
st.title("European Option Pricer")
st.caption("Sigma from rolling historical volatility (log returns).")

# ---------------- Sidebar ----------------
st.sidebar.header("Pricing method")
pricing_method = st.sidebar.selectbox(
    "Method",
    ["Black-Scholes", "Monte Carlo", "Binomial Tree"],
    index=0
)
n_simulations = None
if pricing_method.startswith("Monte Carlo"):
    n_simulations = st.sidebar.number_input(
        "Monte Carlo simulations",
        min_value=1000,
        max_value=2000000,
        value=200000,
        step=10000,
        help="More simulations increase stability but take longer."
    )
binomial_steps = None
american = False
if pricing_method == "Binomial Tree":
    binomial_steps = st.sidebar.number_input(
        "Binomial steps (N)",
        min_value=10,
        max_value=2000,
        value=200,
        step=10,
        help="More steps approximate continuous time better."
    )
    american = st.sidebar.checkbox(
        "American style (early exercise)",
        value=False,
        help="Enable early exercise for American options."
    )

st.sidebar.header("Market data")
ticker = st.sidebar.text_input("Ticker", value="AAPL")
period = st.sidebar.selectbox("History period", ["6mo", "1y", "2y", "5y"], index=1)
use_adj_close = st.sidebar.checkbox("Use Adj Close", value=True)

window = st.sidebar.number_input("Rolling window (days)", min_value=5, max_value=252, value=30, step=1)
trading_days = st.sidebar.number_input("Trading days/year", min_value=200, max_value=365, value=252, step=1)

st.sidebar.header("Option inputs")
option_type = st.sidebar.selectbox("Option type", ["call", "put"], index=0)
K = st.sidebar.number_input("Strike (K)", min_value=0.01, value=180.0, step=1.0)
T_days = st.sidebar.number_input("Maturity (days)", min_value=1, value=180, step=1)
T = T_days / 365.0

r = st.sidebar.number_input("Risk-free rate r (annual, decimal)", value=0.03, step=0.005, format="%.4f")
q = st.sidebar.number_input("Dividend yield q (annual, decimal)", value=0.00, step=0.005, format="%.4f")

st.sidebar.header("Sigma choice")
sigma_choice = st.sidebar.radio(
    "Use which sigma?",
    ["Latest rolling sigma", "Pick a date from rolling sigma", "Manual sigma"],
    index=0
)

manual_sigma = None
if sigma_choice == "Manual sigma":
    manual_sigma = st.sidebar.number_input("Sigma (annual, decimal)", value=0.25, step=0.01, format="%.4f")

st.sidebar.header("Worthiness settings")
min_time_value_ratio = st.sidebar.number_input(
    "Min time-value share (decimal)",
    min_value=0.0,
    max_value=1.0,
    value=0.10,
    step=0.01,
    format="%.2f",
    help="Fraction of premium that should be time value."
)
min_time_value_abs = st.sidebar.number_input(
    "Min time-value absolute",
    min_value=0.0,
    value=0.0,
    step=0.05,
    format="%.4f",
    help="Minimum time value in absolute terms."
)

# ✅ Button
calculate = st.sidebar.button("Calculate", type="primary")

# ---------------- Calculation block ----------------
def run_pricing():
    S = get_spot_price(ticker)

    roll = rolling_hist_vol(
        ticker=ticker,
        period=period,
        use_adj_close=use_adj_close,
        trading_days=int(trading_days),
        window=int(window),
    ).dropna()

    if roll.empty and sigma_choice != "Manual sigma":
        raise ValueError("Rolling sigma series is empty. Try a longer period or smaller window.")

    # choose sigma
    if sigma_choice == "Latest rolling sigma":
        sigma = float(roll.iloc[-1])
        sigma_msg = f"Using latest rolling sigma: {sigma:.4f}"

    elif sigma_choice == "Pick a date from rolling sigma":
        last_n = min(120, len(roll))
        roll_tail = roll.iloc[-last_n:]
        # store selectable dates
        dates = [d.date() for d in roll_tail.index]
        # default last
        chosen = st.session_state.get("chosen_sigma_date", dates[-1])
        chosen = st.selectbox("Pick a date (last points)", dates, index=dates.index(chosen))
        st.session_state["chosen_sigma_date"] = chosen

        idx = next(i for i, d in enumerate(roll_tail.index) if d.date() == chosen)
        sigma = float(roll_tail.iloc[idx])
        sigma_msg = f"Using sigma on {chosen}: {sigma:.4f}"
    else:
        sigma = float(manual_sigma)
        sigma_msg = f"Using manual sigma: {sigma:.4f}"

    # pricing by method
    if pricing_method == "Black-Scholes":
        bs = BlackScholes(S=S, K=K, T=T, r=r, sigma=sigma, option_type=option_type, q=q)
        price = bs.price()
    elif pricing_method == "Binomial Tree":
        steps = int(binomial_steps) if binomial_steps is not None else 200
        price = binomial_tree_option_price(
            S=S,
            K=K,
            T=T,
            r=r,
            sigma=sigma,
            option_type=option_type,
            q=q,
            N=steps,
            american=bool(american),
        )
    elif pricing_method.startswith("Monte Carlo"):
        sims = int(n_simulations) if n_simulations is not None else 200000
        price = montecarlo_simulation_european_option(
            S=S, K=K, T=T, r=r, sigma=sigma, option_type=option_type, q=q,
            n_simulations=sims,
            seed=42
        )
    else:
        raise NotImplementedError("Binomial Tree pricing not implemented yet.")

    worthiness = assess_worthiness(
        S=S,
        K=K,
        premium=price,
        option_type=option_type,
        min_time_value_ratio=float(min_time_value_ratio),
        min_time_value_abs=float(min_time_value_abs),
    )

    inputs = {
        "S": S,
        "roll": roll,
        "sigma": sigma,
        "sigma_msg": sigma_msg,
        "price": price,
        "worthiness": worthiness,
        "inputs": {
            "ticker": ticker,
            "method": pricing_method,
            "type": option_type,
            "K": float(K),
            "T_years": float(T),
            "r": float(r),
            "q": float(q),
            "sigma": float(sigma),
            "window": int(window),
            "period": period,
            "min_time_value_ratio": float(min_time_value_ratio),
            "min_time_value_abs": float(min_time_value_abs),
        },
    }
    if n_simulations is not None:
        inputs["inputs"]["n_simulations"] = int(n_simulations)
    if binomial_steps is not None:
        inputs["inputs"]["binomial_steps"] = int(binomial_steps)
        inputs["inputs"]["american"] = bool(american)

    return inputs


# Only compute when button pressed (or if we already have results)
if calculate:
    try:
        with st.spinner("Calculating..."):
            st.session_state["result"] = run_pricing()
    except Exception as e:
        st.session_state.pop("result", None)
        st.error(f"Error: {e}")

# ---------------- Display (if we have results) ----------------
if "result" in st.session_state:
    res = st.session_state["result"]

    st.subheader("Market inputs")
    st.write({"Ticker": res["inputs"]["ticker"], "Spot (S)": round(res["S"], 4)})

    st.subheader("Rolling historical volatility (annualized)")
    st.write(f"Series length: {len(res['roll'])} points | Window: {res['inputs']['window']} days | Period: {res['inputs']['period']}")

    fig = plt.figure()
    plt.plot(res["roll"].index, res["roll"].values)
    plt.title("Rolling sigma (annualized)")
    plt.xlabel("Date")
    plt.ylabel("Sigma")
    st.pyplot(fig)

    st.info(res["sigma_msg"])

    st.subheader("Option price")
    st.metric(label=f"{res['inputs']['method']} — {res['inputs']['type'].upper()} price", value=f"{res['price']:.4f}")

    st.subheader("Option worthiness")
    w = res.get("worthiness")
    if w:
        verdict = "Worth it" if w["worth_it"] else "Mostly intrinsic value"
        st.metric("Verdict", verdict)
        st.write({
            "Intrinsic value": round(w["intrinsic_value"], 4),
            "Time value": round(w["time_value"], 4),
            "Time value share": f"{w['time_value_ratio']:.1%}",
            "Intrinsic share": f"{w['intrinsic_ratio']:.1%}",
            "Min time-value share": f"{w['inputs']['min_time_value_ratio']:.0%}",
            "Min time-value abs": round(w['inputs']['min_time_value_abs'], 4),
        })
        st.info(w["explanation"])

    st.subheader("Inputs used")
    st.write(res["inputs"])
else:
    st.info("Set your inputs and click **Calculate**.")
