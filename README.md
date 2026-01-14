# Machine Learning projects

Collection of small ML/analytics projects. 

Additional notes live in this [Word document](https://1drv.ms/w/c/10af51fc8c522edd/IQDRqUdJRGfOQbgFIDqMBxqzAehoQYSlhuED0ui4cX1E0uE).

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
- Data is local (`data/BankChurners.csv`); no downloads required. Summary metrics (SMOTE + PCA): ROC-AUC Random Forest 0.97, Recall 0.97, Precision 0.53 on original imbalanced data. See `ChurnPredictor/README.md` for full details.

### Credit Score Model
- Credit risk PD modeling on consumer loans (`CreditScore/loans_full_schema.csv`); filtered to final outcomes (Fully Paid vs Charged Off) → 454 loans with ~1.54% defaults, so evaluation focuses on minority-class metrics rather than accuracy.
- EDA highlights: income mostly 0–50k, DTI 0–50; defaults rare across numerics but higher for borrowers with mortgages, tax liens (~14% vs ~1.35% when absent), and housing-related loan purposes. Rare-event nature makes calibration and threshold tuning critical.
- Feature selection keeps application-time, interpretable variables: `annual_income`, `debt_to_income`, `homeownership`, `emp_length`, `verified_income`, `earliest_credit_line`, `total_credit_lines`, `open_credit_lines`, `months_since_last_delinq`, `public_record_bankrupt`, `tax_liens`, `loan_amount`, `loan_purpose`, `application_type`; excludes sparse/unstable delinquency counters (`num_historical_failed_to_pay`, `delinq_2yr`, `months_since_90d_late`).
- Next steps (in progress): outlier treatment, scaling/encoding, logistic regression with class weighting + calibration, SHAP explainability, and portfolio simulation. See `CreditScore/03_EDA_Credit_Score.ipynb` and `CreditScore/03_Feature_Selection.ipynb`.

## Roadmap / ideas
- Deepen the European options project: data exploration, Black–Scholes, Monte Carlo, and Binomial tree implementations; benchmark and compare parameter sensitivity.
- Package and deploy the churn model (inference pipeline + API/Streamlit).
- Add visuals/screenshots for churn and credit score projects.
