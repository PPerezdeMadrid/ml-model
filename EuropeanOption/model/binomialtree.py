import numpy as np


def binomial_tree_option_price(
    S: float,
    K: float,
    T: float,
    r: float,
    sigma: float,
    option_type: str = "call",
    N: int = 200,
    q: float = 0.0,
    american: bool = False,
):
    """
    Price a European or American option using the Cox-Ross-Rubinstein (CRR) binomial tree.

    Parameters:
    S : float
        Spot price.
    K : float
        Strike price.
    T : float
        Time to maturity in years.
    r : float
        Risk-free rate (continuously compounded).
    sigma : float
        Volatility (annualised).
    option_type : str
        "call" or "put".
    N : int
        Number of time steps in the tree.
    q : float
        Continuous dividend yield (annualised). Default 0.0.
    american : bool
        If True, price an American option (early exercise allowed).
        If False, price a European option.
    """
    
    if S <= 0 or K <= 0:
        raise ValueError("S and K must be positive.")
    if T <= 0:
        raise ValueError("T must be positive (in years).")
    if sigma < 0:
        raise ValueError("sigma must be non-negative.")
    if N <= 0:
        raise ValueError("N must be a positive integer.")

    opt = option_type.strip().lower()
    if opt not in ("call", "put"):
        raise ValueError("option_type must be 'call' or 'put'.")

    # 1) Time step 
    dt = T / N

    # 2) Up/Down factors (CRR) 
    # u > 1, d < 1 and recombining: d = 1/u
    u = np.exp(sigma * np.sqrt(dt))
    d = 1.0 / u

    #  3) Risk-neutral probability (no-arbitrage) 
    # Under risk-neutral measure, expected growth is (r - q)
    disc = np.exp(-r * dt)
    growth = np.exp((r - q) * dt)

    p = (growth - d) / (u - d)

    # Numerical guard: if p is outside [0,1], something is inconsistent
    if not (0.0 <= p <= 1.0):
        raise ValueError(
            f"Risk-neutral probability p={p:.4f} is outside [0,1]. "
            "Check inputs (sigma, r, q, T, N)."
        )

    #  4) Terminal underlying prices S_T at maturity 
    # At step N, possible prices are: S * u^j * d^(N-j), j=0..N (j = number of up moves)
    j = np.arange(N + 1)
    S_T = S * (u ** j) * (d ** (N - j))

    #  5) Terminal payoffs 
    if opt == "call":
        values = np.maximum(S_T - K, 0.0)
    else:
        values = np.maximum(K - S_T, 0.0)

    #  6) Backward induction 
    # Move backwards from time N to 0
    for step in range(N - 1, -1, -1):
        # Continuation value (European logic)
        values = disc * (p * values[1:] + (1.0 - p) * values[:-1])

        if american:
            # Recompute underlying prices at this step to check early exercise
            j = np.arange(step + 1)
            S_step = S * (u ** j) * (d ** (step - j))

            if opt == "call":
                intrinsic = np.maximum(S_step - K, 0.0)
            else:
                intrinsic = np.maximum(K - S_step, 0.0)

            # American option: value is max(exercise now, hold)
            values = np.maximum(values, intrinsic)

    # values[0] is the option price at the root node
    return float(values[0])
