# 💳 Personal Finance Anomaly Detector

An AI/ML-based personal finance analytics project that detects unusual financial transactions using **Python, Pandas, Scikit-learn, and Isolation Forest**.

The project currently focuses on building the complete data pipeline, generating realistic transaction data, performing feature engineering, and detecting potentially anomalous transactions.

---

## 🚀 Project Overview

Managing personal expenses manually can make it difficult to identify unusual or suspicious transactions.

The **Personal Finance Anomaly Detector** analyzes transaction data and identifies transactions that differ significantly from normal spending patterns.

The current system:

- Generates a synthetic financial transaction dataset
- Preprocesses transaction data
- Performs feature engineering
- Encodes categorical information
- Trains an Isolation Forest anomaly detection model
- Calculates anomaly scores
- Identifies potentially unusual transactions
- Saves the trained ML model
- Exports anomaly detection results for further analysis

---

## 🏗️ Current Project Architecture

```text
Transaction Data
       │
       ▼
generate_data.py
       │
       ▼
transactions.csv
       │
       ▼
preprocess.py
       │
       ▼
processed_transactions.csv
       │
       ▼
Feature Engineering
       │
       ▼
train_model.py
       │
       ▼
Isolation Forest
       │
       ├──────────────► isolation_forest.pkl
       │
       ▼
Anomaly Detection
       │
       ▼
anomaly_results.csv
