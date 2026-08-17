import pandas as pd
import joblib

from pathlib import Path
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder


# -----------------------------
# Project paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed_transactions.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_FILE = MODEL_DIR / "isolation_forest.pkl"

MODEL_DIR.mkdir(exist_ok=True)


# -----------------------------
# Load processed dataset
# -----------------------------
df = pd.read_csv(INPUT_FILE)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# -----------------------------
# Encode categorical columns
# -----------------------------
category_encoder = LabelEncoder()
merchant_encoder = LabelEncoder()
payment_encoder = LabelEncoder()

df["category_encoded"] = category_encoder.fit_transform(
    df["category"]
)

df["merchant_encoded"] = merchant_encoder.fit_transform(
    df["merchant"]
)

df["payment_encoded"] = payment_encoder.fit_transform(
    df["payment_method"]
)


# -----------------------------
# Select features for anomaly detection
# -----------------------------
features = [
    "amount",
    "amount_log",
    "amount_vs_category_avg",
    "day",
    "month",
    "day_of_week",
    "is_weekend",
    "category_encoded",
    "merchant_encoded",
    "payment_encoded"
]

X = df[features]


print("\nFeatures used for training:")
for feature in features:
    print("-", feature)


# -----------------------------
# Create Isolation Forest
# -----------------------------
model = IsolationForest(
    n_estimators=200,
    contamination=0.03,
    random_state=42,
    n_jobs=-1
)


# -----------------------------
# Train model
# -----------------------------
model.fit(X)

print("\nIsolation Forest model trained successfully!")


# -----------------------------
# Predict anomalies
# -----------------------------
df["anomaly_prediction"] = model.predict(X)

df["anomaly_score"] = model.decision_function(X)


# Isolation Forest:
# -1 = anomaly
#  1 = normal

df["is_anomaly"] = (
    df["anomaly_prediction"] == -1
).astype(int)


# -----------------------------
# Save model
# -----------------------------
joblib.dump(model, MODEL_FILE)

print(f"\nModel saved successfully!")
print(f"Model file: {MODEL_FILE}")


# -----------------------------
# Display results
# -----------------------------
total_anomalies = df["is_anomaly"].sum()
total_transactions = len(df)

print("\nAnomaly Detection Results")
print("-------------------------")
print("Total transactions:", total_transactions)
print("Anomalies detected:", total_anomalies)
print(
    "Anomaly percentage:",
    round((total_anomalies / total_transactions) * 100, 2),
    "%"
)


# -----------------------------
# Save results
# -----------------------------
OUTPUT_FILE = BASE_DIR / "outputs" / "anomaly_results.csv"

OUTPUT_FILE.parent.mkdir(exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)

print(f"\nResults saved to:")
print(OUTPUT_FILE)