import joblib
import pandas as pd

# Load once
model = joblib.load("app/ml_models/expense_classifier.joblib")

def normalize_category(raw_category):
    if raw_category in ["Fixed", "Utilities", "Insurance"]:
        return "Fixed"
    elif raw_category in ["Transport", "Food", "Entertainment", "Health", "Luxury"]:
        return "Variable"
    else:
        return "Variable"

def classify_expenses(df: pd.DataFrame) -> pd.DataFrame:
    df.rename(columns={"description": "Description", "amount": "Amount"}, inplace=True)
    df["category"] = model.predict(df[["Description", "Amount"]])
    df["category"] = df["category"].apply(normalize_category)
    return df

