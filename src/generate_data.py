import pandas as pd
import numpy as np
from pathlib import Path


# -----------------------------
# Configuration
# -----------------------------
np.random.seed(42)

NUM_TRANSACTIONS = 10000


# -----------------------------
# Create project paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = DATA_DIR / "transactions.csv"


# -----------------------------
# Generate transaction data
# -----------------------------
dates = pd.date_range(
    start="2025-01-01",
    end="2026-06-30",
    periods=NUM_TRANSACTIONS
)

categories = [
    "Food",
    "Transport",
    "Shopping",
    "Entertainment",
    "Bills",
    "Healthcare",
    "Education",
    "Travel"
]

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Cash"
]

merchants = [
    "Amazon",
    "Swiggy",
    "Zomato",
    "Uber",
    "Flipkart",
    "Myntra",
    "Netflix",
    "Airtel",
    "Reliance",
    "Local Store"
]


data = {
    "transaction_id": range(1, NUM_TRANSACTIONS + 1),
    "date": dates,
    "category": np.random.choice(
        categories,
        NUM_TRANSACTIONS
    ),
    "merchant": np.random.choice(
        merchants,
        NUM_TRANSACTIONS
    ),
    "amount": np.round(
        np.random.uniform(50, 5000, NUM_TRANSACTIONS),
        2
    ),
    "payment_method": np.random.choice(
        payment_methods,
        NUM_TRANSACTIONS
    )
}


df = pd.DataFrame(data)


# -----------------------------
# Add some realistic anomalies
# -----------------------------
anomaly_indices = np.random.choice(
    df.index,
    size=30,
    replace=False
)

df.loc[anomaly_indices, "amount"] *= np.random.uniform(
    5,
    15,
    size=len(anomaly_indices)
)

df["amount"] = df["amount"].round(2)


# -----------------------------
# Save dataset
# -----------------------------
df.to_csv(OUTPUT_FILE, index=False)

print("Dataset generated successfully!")
print(f"File saved at: {OUTPUT_FILE}")
print(f"Total transactions: {len(df)}")
print("\nFirst 5 transactions:")
print(df.head())