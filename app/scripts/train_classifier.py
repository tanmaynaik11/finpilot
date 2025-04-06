import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib

# Load updated dataset
df = pd.read_csv("data/expenses_labeled.csv")

# Features
X = df[["Description", "Amount"]]
y = df["Category"]

# Preprocessing pipeline
preprocessor = ColumnTransformer([
    ("desc", TfidfVectorizer(), "Description"),
    ("amt", StandardScaler(), ["Amount"])
])

# ML pipeline
pipeline = Pipeline([
    ("preprocess", preprocessor),
    ("clf", LogisticRegression(max_iter=500))
])

pipeline.fit(X, y)

# Save model
joblib.dump(pipeline, "app/ml_models/expense_classifier.joblib")
print("✅ Model trained and saved!")
