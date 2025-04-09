import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from xgboost import XGBClassifier

# ✅ Pad naar de dummy dataset (pas aan indien nodig)
df = pd.read_csv("../data/dummy_network_logs.csv")

# ✅ Selecteer relevante features
features = [
    "source.ip", "destination.ip", "source.port", "destination.port",
    "network.transport", "session.iflow_bytes", "session.iflow_pkts"
]
X = df[features]
y = df["label"]

# ✅ Encode string features (IP-adressen, protocol)
encoders = {}
for col in ["source.ip", "destination.ip", "network.transport"]:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    encoders[col] = le

# ✅ Zorg dat alle kolommen numeriek zijn
X["source.port"] = pd.to_numeric(X["source.port"], errors="coerce")
X["destination.port"] = pd.to_numeric(X["destination.port"], errors="coerce")
X["session.iflow_bytes"] = pd.to_numeric(X["session.iflow_bytes"], errors="coerce")
X["session.iflow_pkts"] = pd.to_numeric(X["session.iflow_pkts"], errors="coerce")

# ✅ Vul eventuele ontbrekende waarden op
X = X.fillna(0)

# ✅ Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Train modellen
print("=== Random Forest ===")
rf = RandomForestClassifier(random_state=42)
rf.fit(X_train, y_train)
rf_preds = rf.predict(X_test)
print(classification_report(y_test, rf_preds))

print("=== Logistic Regression ===")
lr = LogisticRegression(max_iter=1000)
lr.fit(X_train, y_train)
lr_preds = lr.predict(X_test)
print(classification_report(y_test, lr_preds))

print("=== XGBoost ===")
xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
xgb.fit(X_train, y_train)
xgb_preds = xgb.predict(X_test)
print(classification_report(y_test, xgb_preds))


import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

# === Confusion Matrix plotten voor Random Forest ===
cm = confusion_matrix(y_test, rf_preds)

plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=["Normaal", "Anomalie"], yticklabels=["Normaal", "Anomalie"])
plt.xlabel("Voorspeld label")
plt.ylabel("Echte label")
plt.title("Confusion Matrix - Random Forest")
plt.tight_layout()
#plt.show()



import joblib

# Sla de getrainde modellen op
joblib.dump(rf, "../models/random_forest_model.pkl")
joblib.dump(lr, "../models/logistic_regression_model.pkl")
joblib.dump(xgb, "../models/xgboost_model.pkl")

#Sla de encoders op (later nodig bij preprocessing van echte data)
for col, encoder in encoders.items():
    joblib.dump(encoder, f"../models/encoder_{col}.pkl")

print("Modellen en encoders opgeslagen!")
