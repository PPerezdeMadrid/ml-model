"""
MonteCarlo simulation for European Option pricing.
"""

import numpy as np

def montecarlo_simulation_european_option(
        S: float,
        K: float,
        T: float,
        r: float,
        sigma: float,
        option_type: str = "call",
        q: float = 0.0,
        n_simulations: int = 200000,
        seed: int = 42
):
    """
    Monte Carlo pricer for European options under Geometric Brownian Motion (GBM).
    Parameters: 
        S (Spot price today), K (Strike price) T (Time to maturity in years), r (Risk-free interest rate (annualised, continuously compounded)),
        sigma (Volatility (annualised)), option_type ("call" or "put"), q (Continuous dividend yield (annualised). Default 0.0.),
        n_simulations (Number of Monte Carlo simulations.), seed (Random seed for reproducibility. Use None for non-deterministic runs.)
    """

    if S <= 0 or K <= 0:
        raise ValueError("S and K must be positive.")
    if T <= 0:
        raise ValueError("T must be positive (in years).")
    if sigma < 0:
        raise ValueError("sigma must be non-negative.")
    if n_simulations <= 0:
        raise ValueError("n_simulations must be positive.")
    
    opt = option_type.strip().lower()
    if opt not in ("call", "put"):
        raise ValueError("option_type must be 'call' or 'put'.")

    rng = np.random.default_rng(seed=seed)

    # Step 1 — Generate random shocks Z ~ N(0,1)
    Z = rng.standard_normal(n_simulations)

    # Step 2 — Simulate terminal prices under risk-neutral measure
    # S_T = S * exp((r - q - 0.5*sigma^2)*T + sigma*sqrt(T)*Z)
    drift = (r - q - 0.5*sigma**2)
    diffusion = sigma * np.sqrt(T) * Z
    S_T = S * np.exp(drift + diffusion)

    # Step 3 — Compute payoffs
    if opt == "call":
        payoffs = np.maximum(S_T -K, 0.0) 
    else:
        payoffs = np.minimum(K - S_T, 0.0 )

    # Step 4 — Average payoffs and discount back
    discounted_payoff_mean = np.mean(payoffs) * np.exp(-r * T)

    return float(discounted_payoff_mean)

