# Customer Engagement & Product Utilization Analytics for Retention Strategy

Churn analysis of 10,000 retail banking customers, built during my EuroBank ML internship.

## What's inside
- `churn_analysis.ipynb`: EDA, engagement segmentation, 5 retention KPIs, and model comparison (Logistic Regression, Random Forest, Gradient Boosting)
- `app.py`: Streamlit dashboard
- `model.pkl`: trained Gradient Boosting pipeline
- `requirements.txt`: dependencies

## Key findings
- Active customers with multiple products churn at 9.7%; inactive customers with high balances churn at 32.3%
- Gradient Boosting: ~86.3% test accuracy, ROC-AUC 0.87

## Run the dashboard
pip install -r requirements.txt
streamlit run app.py

## Paper
Gaikwad, Manas. "Customer Engagement and Product Utilization Analytics for Retention Strategy." Zenodo, 2026. https://doi.org/10.5281/zenodo.23096725

## Dataset
(Name the source here, or say where to download European_Bank.csv.)
