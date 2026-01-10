# Churn Predictor

Bank customer churn classification on the BankChurners dataset (Kaggle, Thomas Konstantin). 
> Goal: predict whether a  customer will attrite to guide retention actions.

## Dataset
- Source: BankChurners.csv (included). 10,127 customers, 21 features, no missing values.
- Target: Attrition_Flag with classes Attrited Customer vs Existing Customer; moderate class imbalance (~15-20% churn).
- Feature groups: demographics (age, gender, dependents, education, marital status, income), relationship data (months on book, products, card category), credit profile (credit limit, revolving balance, utilization), transactions (total amount and count, quarterly change).
- Removed before modeling to avoid leakage: CLIENTNUM and the two Naive_Bayes_Classifier probability columns.

## Notebooks
- 02_EDA_Churn_predictor.ipynb: churn distribution, demographic and behavior patterns, correlation and boxplot insights, EDA-level feature importance.
- 02_Data_Preprocessing_Churn_predictor.ipynb: pipeline order clarifications, train/test split, one-hot encoding, SMOTE upsampling, scaling, optional PCA retaining 95 percent variance.
- 02_Model_Churn_predictor.ipynb: cross-validation comparing Logistic Regression, Random Forest, Gradient Boosting, and XGBoost on the SMOTE + PCA set.
- 02_Results_Churn_predictor.ipynb: holdout and imbalance-aware evaluation, classification reports, ROC-AUC, confusion matrices.
- 02_Improvements_Churn_predictor.ipynb: threshold tuning to balance precision and recall; reducing SMOTE ratio to limit over-sensitisation to the minority class.

## Modeling pipeline
- Split: approx 80/20 (train 8,101; test 2,026).
- Encoding: one-hot on categorical features; fit on train then applied to test.
- Class balance: SMOTE applied on training data prior to scaling and PCA (train after SMOTE 13,598 rows).
- Scaling: standardization for PCA and linear models.
- PCA: optional dimensionality reduction keeping 95 percent variance (train shape after PCA 13,598 x 22; test 2,026 x 22).
- Models: Logistic Regression, Random Forest, Gradient Boosting, XGBoost.

## Results
Cross-validation (SMOTE + PCA):
- ROC-AUC: Logistic Regression 0.892; Random Forest 0.983; Gradient Boosting 0.950; XGBoost 0.965.
- F1 score: 0.818; 0.935; 0.880; 0.901 respectively.
Test set (SMOTE + PCA) with Random Forest:
- Accuracy 0.80; ROC-AUC 0.895.
- Attrited Customer precision 0.44, recall 0.84 (confusion matrix [[274, 51], [355, 1346]]).
Evaluation on original imbalanced training data (Random Forest):
- Accuracy 0.85; ROC-AUC 0.973; attrited recall 0.97 vs precision 0.53.

## How to run
- Python 3.10+ recommended. Dependencies in ../requirements.txt (numpy, pandas, scikit-learn, imblearn, xgboost, streamlit for other project).
- Create env and install:
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r ../requirements.txt
- If xgboost fails on macOS: brew install libomp.
- Open notebooks from ml-model/ChurnPredictor and run in order: EDA -> Data Preprocessing -> Model -> Results. Data file is local, no downloads required.

## Ideas to extend
- Tune decision thresholds to improve precision vs recall trade-off.
- Add SHAP or permutation importance for model explainability.
- Package the preprocessing pipeline with the best model for inference (e.g., joblib and a FastAPI/Streamlit endpoint).
- Monitor drift and retrain cadence once deployed.
