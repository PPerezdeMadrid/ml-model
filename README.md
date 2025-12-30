# ml-model
Different projects to train as a Data Scientist

based on https://github.com/just-krivi/option-pricing-models


# Project: European Option 

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
- Build clean, well-documented, and reusable Python code suitable for a quantitative finance portfolio.


## Technology Stack
ToDo

## Repository Structure
```
pricing-model/
│
├── data/
│   ├── raw/                # Source Data
│   ├── processed/          # Clean Data/ features
│
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_FeatureEngineering.ipynb
│   ├── 03_Modeling.ipynb
│   └── 04_Evaluation.ipynb
│
├── src/
│   ├── utils.py
│   ├── preprocessing.py
│   ├── modeling.py
│
├── reports/
│   ├── figures/            # Visualisations
│   └── metrics/            # Results
│
├── README.md
├── requirements.txt
└── .gitignore
```

## Results
- **Main metric:** AUC / Accuracy / F1 / ROC
- **Estimated impact:** churn reduction of X%, risk improvement of Y%, etc.
- **Most influential variables:** interpreted list using SHAP.

## Conclusions
Summary of findings + business recommendations.

## Next Steps
Ideas to improve the model or integrate it into production. 
