# graphs.py
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from feature_engineering import build_features
data = pd.read_csv("synthetic_studentlife_stress_data.csv")

features = joblib.load("artifacts/features.pkl")
model = joblib.load("artifacts/model.pkl")
y_prob = np.load("artifacts/y_prob.npy")

y = data["stress_label"]

# ROC Curve
fpr, tpr, _ = roc_curve(y, y_prob)
roc_auc = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.3f}")
plt.plot([0,1],[0,1],'--')
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC–AUC Curve")
plt.legend()
plt.show()

# Feature importance
importances = model.named_steps["clf"].feature_importances_

plt.figure()
plt.barh(features, importances)
plt.title("Feature Importance")
plt.show()