import pandas as pd
import joblib
import os

# === 1. Laad de echte dataset ===
df = pd.read_csv(
    r"C:\Users\laure\PycharmProjects\Data-Driven Anomaly Detection\data\Dag_data.csv",
    on_bad_lines='skip',
    low_memory=False
)

# === 2. Selecteer relevante features ===
relevant_columns = [
    "source.ip", "destination.ip", "source.port", "destination.port",
    "network.transport", "session.iflow_bytes", "session.iflow_pkts"
]
df_selected = df[relevant_columns].copy()

# === 3. Laad encoders en pas toe met fallback (-1) voor onbekende waarden ===
encoders = {}
for col in ["source.ip", "destination.ip", "network.transport"]:
    encoder_path = f"../models/encoder_{col}.pkl"
    if os.path.exists(encoder_path):
        enc = joblib.load(encoder_path)
        encoders[col] = enc

        # Zet om naar string en encodeer, onbekende waarden → -1
        df_selected[col] = df_selected[col].astype(str)
        known_classes = set(enc.classes_)
        df_selected[col] = df_selected[col].apply(lambda x: enc.transform([x])[0] if x in known_classes else -1)
    else:
        raise FileNotFoundError(f"Encoder voor kolom {col} niet gevonden.")

# === 4. Zet numerieke kolommen correct om ===
for col in ["source.port", "destination.port", "session.iflow_bytes", "session.iflow_pkts"]:
    df_selected[col] = pd.to_numeric(df_selected[col], errors="coerce")

df_selected.dropna(inplace=True)

# === 5. Check of er nog rijen zijn ===
if df_selected.empty:
    raise ValueError("Geen geldige rijen over na encoding en filtering.")

# === 6. Laad modellen ===
rf_model = joblib.load("../models/random_forest_model.pkl")
log_model = joblib.load("../models/logistic_regression_model.pkl")
xgb_model = joblib.load("../models/xgboost_model.pkl")

# === 7. Kopieer per model om kolomconflict te vermijden ===
df_rf = df_selected.copy()
df_log = df_selected.copy()
df_xgb = df_selected.copy()

# === 8. Voorspellingen maken ===
df_rf["RF_pred"] = rf_model.predict(df_rf)
df_log["LOG_pred"] = log_model.predict(df_log)
df_xgb["XGB_pred"] = xgb_model.predict(df_xgb)

# === 9. Aantallen tonen ===
print("Aantal voorspelde anomalieën:")
print("🔍 Random Forest:", (df_rf["RF_pred"] == 1).sum())
print("🔍 Logistic Regression:", (df_log["LOG_pred"] == 1).sum())
print("🔍 XGBoost:", (df_xgb["XGB_pred"] == 1).sum())

# === 10. Toon de eerste 10 anomalieën van elk model ===
print("\n🔎 Random Forest anomalieën:")
print(df_rf[df_rf["RF_pred"] == 1].head(10))

print("\n🔎 Logistic Regression anomalieën:")
print(df_log[df_log["LOG_pred"] == 1].head(10))

print("\n🔎 XGBoost anomalieën:")
print(df_xgb[df_xgb["XGB_pred"] == 1].head(10))
