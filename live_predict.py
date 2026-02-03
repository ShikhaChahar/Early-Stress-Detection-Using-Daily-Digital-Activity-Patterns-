import joblib
import pandas as pd

from google_fit_fetcher import fetch_google_fit_data
from feature_engineering import build_features

# -------------------------------
# Load trained model
# -------------------------------
model = joblib.load("artifacts/model.pkl")

# -------------------------------
# Fetch Google Fit data
# -------------------------------
fit_data = fetch_google_fit_data()

# -------------------------------
# Map Google Fit data → Model input
# -------------------------------
mapped_data = {
    "screen_time": fit_data.get("sedentary_minutes", 600),  # proxy
    "app_sessions": 100,                                    # average assumption
    "night_usage": max(0, 480 - fit_data["sleep_hours"] * 60),
    "call_count": 5,
    "sms_count": 20,
    "sleep_hours": fit_data["sleep_hours"],
    "app_entropy": 1.5
}

df = pd.DataFrame([mapped_data])

# -------------------------------
# Feature engineering
# -------------------------------
X = build_features(df)

# -------------------------------
# Predict stress risk
# -------------------------------
risk_score = model.predict_proba(X)[0][1]

# -------------------------------
# Interpret result
# -------------------------------
if risk_score < 0.3:
    status = "Low Stress Risk"
elif risk_score < 0.6:
    status = "Moderate Stress Risk"
else:
    status = "High Stress Risk"

print("\n📊 Current Stress Assessment")
print("-----------------------------")
print(f"Stress Risk Score : {risk_score:.2f}")
print(f"Status            : {status}")
