import pandas as pd
from pathlib import Path


# -----------------------------
# Project paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "transactions.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed_transactions.csv"


# -----------------------------
# Load dataset
# -----------------------------
df = pd.read_csv(INPUT_FILE)

print("Original dataset shape:", df.shape)


# -----------------------------
# Convert date column
# -----------------------------
df["date"] = pd.to_datetime(df["date"])


# -----------------------------
# Create date-based features
# -----------------------------
df["day"] = df["date"].dt.day
df["month"] = df["date"].dt.month
df["year"] = df["date"].dt.year
df["day_of_week"] = df["date"].dt.dayofweek
df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)


# -----------------------------
# Create transaction features
# -----------------------------
df["amount_log"] = __import__("numpy").log1p(df["amount"])

df["category_avg_amount"] = (
    df.groupby("category")["amount"]
    .transform("mean")
)

df["amount_vs_category_avg"] = (
    df["amount"] / df["category_avg_amount"]
)


# -----------------------------
# Sort transactions by date
# -----------------------------
df = df.sort_values("date").reset_index(drop=True)


# -----------------------------
# Save processed dataset
# -----------------------------
df.to_csv(OUTPUT_FILE, index=False)

print("Processed dataset saved successfully!")
print(f"File: {OUTPUT_FILE}")
print("Processed dataset shape:", df.shape)

print("\nNew columns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())