"""
Module to compute the intrinsic value of European options.
"""

def intrinsic_value(S: float, K: float, option_type: str) -> float:
    """
    Intrinsic value if the option expired right now.
    """
    opt = option_type.strip().lower()
    if opt == "call":
        return max(S - K, 0.0)
    if opt == "put":
        return max(K - S, 0.0)
    raise ValueError("option_type must be 'call' or 'put'")

def assess_worthiness(
    S: float,
    K: float,
    premium: float,
    option_type: str,
    min_time_value_ratio: float = 0.10,
    min_time_value_abs: float = 0.0,
):
    """
    Assess whether an option seems 'worth it' based on how much of the premium
    is paying for optionality (time value) vs intrinsic value.

    Heuristic:
    - If most of what you pay is intrinsic value, the option behaves like the stock
      and offers limited convexity per euro.
    - We flag it as "worth_it" only if:
        time_value / premium >= min_time_value_ratio
      AND time_value >= min_time_value_abs

    Parameters
    ----------
    S, K : float
        Spot and strike.
    premium : float
        Option price returned by any model (BS, Monte Carlo, etc.).
    option_type : str
        "call" or "put".
    min_time_value_ratio : float
        Minimum fraction of premium that should be time value (e.g., 0.10 = 10%).
    min_time_value_abs : float
        Minimum time value in absolute terms (useful for tiny premiums).
    """
    if premium <= 0:
        raise ValueError("premium must be positive.")

    intrinsic = intrinsic_value(S, K, option_type)
    time_value = max(premium - intrinsic, 0.0)

    time_value_ratio = time_value / premium  # fraction of premium buying uncertainty
    intrinsic_ratio = intrinsic / premium

    # Simple flags
    deep_itm_like = time_value_ratio < 0.08  # very low optionality share
    worth_it = (time_value_ratio >= min_time_value_ratio) and (time_value >= min_time_value_abs)

    explanation_parts = []
    explanation_parts.append(
        f"You pay {premium:.4f}. Intrinsic value is {intrinsic:.4f}, so time value is {time_value:.4f}."
    )
    explanation_parts.append(
        f"Only {time_value_ratio:.1%} of the premium buys optionality (future uncertainty)."
    )

    if deep_itm_like:
        explanation_parts.append(
            "This is a low-optionality trade: most of the premium is intrinsic value, so the option behaves similar to the underlying."
        )

    if worth_it:
        explanation_parts.append(
            f"Based on the chosen threshold (min_time_value_ratio={min_time_value_ratio:.0%}), this looks worth considering."
        )
    else:
        explanation_parts.append(
            f"Based on the chosen threshold (min_time_value_ratio={min_time_value_ratio:.0%}), this looks unattractive for optionality-per-euro."
        )

    return {
        "inputs": {
            "S": S,
            "K": K,
            "premium": premium,
            "option_type": option_type,
            "min_time_value_ratio": min_time_value_ratio,
            "min_time_value_abs": min_time_value_abs,
        },
        "intrinsic_value": intrinsic,
        "time_value": time_value,
        "time_value_ratio": time_value_ratio,
        "intrinsic_ratio": intrinsic_ratio,
        "worth_it": worth_it,
        "explanation": " ".join(explanation_parts),
    }