# train_model.py
import pandas as pd
import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from feature_engineering import build_features

data = pd.read_csv("synthetic_studentlife_stress_data.csv")

data["screen_per_session"] = data["screen_time"] / (data["app_sessions"] + 1)
data["night_screen_ratio"] = data["night_usage"] / (data["screen_time"] + 1)
data["sleep_deficit"] = 8 - data["sleep_hours"]

features = [
    "screen_time","app_sessions","night_usage",
    "call_count","sms_count","sleep_hours","app_entropy",
    "screen_per_session","night_screen_ratio","sleep_deficit"
]

X = data[features]
y = data["stress_label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42
)

model = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", GradientBoostingClassifier(random_state=42))
])

model.fit(X_train, y_train)

# Save artifacts
joblib.dump(model, "artifacts/model.pkl")
joblib.dump(features, "artifacts/features.pkl")

print("Model trained and saved successfully")