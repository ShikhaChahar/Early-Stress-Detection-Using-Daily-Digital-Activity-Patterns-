# evaluate.py
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score
from feature_engineering import build_features

data = pd.read_csv("synthetic_studentlife_stress_data.csv")

model = joblib.load("artifacts/model.pkl")
features = joblib.load("artifacts/features.pkl")


X = build_features(data)
y = data["stress_label"]

y_pred = model.predict(X)
y_prob = model.predict_proba(X)[:, 1]

np.save("artifacts/y_prob.npy", y_prob)

print("Precision :", round(precision_score(y, y_pred), 3))
print("Recall    :", round(recall_score(y, y_pred), 3))
print("F1-Score  :", round(f1_score(y, y_pred), 3))

