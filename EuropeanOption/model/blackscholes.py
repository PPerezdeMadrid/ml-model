import math


class BlackScholes:
    """
    Minimal Black-Scholes model for European options (price only).
    """

    def __init__(self, S, K, T, r, sigma, option_type="call", q=0.0):
        self.S = float(S)          # Spot price
        self.K = float(K)          # Strike price
        self.T = float(T)          # Time to maturity (years)
        self.r = float(r)          # Risk-free rate (continuous)
        self.sigma = float(sigma)  # Volatility (annual)
        self.q = float(q)          # Dividend yield
        self.option_type = option_type.lower()

        if self.option_type not in ("call", "put"):
            raise ValueError("option_type must be 'call' or 'put'.")

    def N(self, x):
        """Standard normal CDF."""
        return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

    def d1(self):
        return (
            math.log(self.S / self.K)
            + (self.r - self.q + 0.5 * self.sigma**2) * self.T
        ) / (self.sigma * math.sqrt(self.T))

    def d2(self):
        return self.d1() - self.sigma * math.sqrt(self.T)

    def price(self):
        d1 = self.d1()
        d2 = self.d2()

        discount_r = math.exp(-self.r * self.T)
        discount_q = math.exp(-self.q * self.T)

        if self.option_type == "call":
            return self.S * discount_q * self.N(d1) - self.K * discount_r * self.N(d2)
        else:
            return self.K * discount_r * self.N(-d2) - self.S * discount_q * self.N(-d1)
