# Machine Learning projects

Collection of small ML/analytics projects. Additional notes live in this [Word document](https://1drv.ms/w/c/10af51fc8c522edd/IQDRqUdJRGfOQbgFIDqMBxqzAehoQYSlhuED0ui4cX1E0uE).

## Repo at a glance
- `EuropeanOption/`: Streamlit + CLI app to price European call/put options with Black-Scholes (historical sigma from Yahoo Finance).
- `ChurnPredictor/`: Bank customer churn classification on the BankChurners dataset (Kaggle, Thomas Konstantin).
- `data/`: datasets used by the projects (e.g., `BankChurners.csv`).
- `requirements.txt`: shared Python dependencies.

## Stack
- Python 3.10+, Jupyter notebooks.
- Core libs: numpy, pandas, matplotlib.
- Modeling: scikit-learn, imblearn (SMOTE), xgboost.
- App/data: streamlit, yfinance, requests, python-dotenv.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```
> If `xgboost` fails on macOS, install `libomp` via Homebrew: `brew install libomp`.

## Projects
### European Option Pricing App
- Based on https://github.com/just-krivi/option-pricing-models.
- Prices European calls/puts using Black-Scholes with volatility estimated from historical prices (yfinance). Streamlit UI plus a small CLI example.
- Run the app from `EuropeanOption/`: `streamlit run streamlit_app.py`. See `EuropeanOption/README.md` for full usage.
![Streamlit demo](EuropeanOption/europeanOption.gif)

### Churn Predictor Model
- Binary classification of bank customer churn; uses one-hot encoding, SMOTE, scaling, optional PCA, and compares Logistic Regression, Random Forest, Gradient Boosting, and XGBoost.
- Notebooks in `ChurnPredictor/` document EDA, preprocessing, modeling, and results. Recommended order: EDA → Data Preprocessing → Model → Results.
- Data is local (`data/BankChurners.csv`); no downloads required. Summary metrics (SMOTE + PCA): ROC-AUC ~0.98 with Random Forest; test accuracy ~0.80.

### Credit Score Model
- Placeholder; add description, data source, and results when available.

## Roadmap / ideas
- Deepen the European options project: data exploration, Black–Scholes, Monte Carlo, and Binomial tree implementations; benchmark and compare parameter sensitivity.
- Package and deploy the churn model (inference pipeline + API/Streamlit).
- Add visuals/screenshots for churn and credit score projects.
