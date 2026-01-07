from model.blackscholes import BlackScholes


bs = BlackScholes(
    S=100,
    K=105,
    T=30/365,
    r=0.03,
    sigma=0.25,
    option_type="call"
)

print(bs.price())
