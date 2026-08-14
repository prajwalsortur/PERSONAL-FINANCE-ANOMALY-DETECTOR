# Personal Finance Anomaly Detector

An AI-powered personal finance tool that automatically identifies unusual spending patterns, suspicious transactions, and abnormal financial behavior from user transaction data — with interactive dashboards for real-time insights.

## Features

- 🔍 **Anomaly detection** — flags unusual spending patterns and suspicious transactions
- 📊 **Interactive dashboards** to visualize spending trends over time
- 🤖 **Machine learning models** trained on transaction data to learn normal vs. abnormal behavior
- 💡 **Personalized financial insights** based on individual spending habits
- ⚡ **Real-time analysis** as new transactions come in

## Tech Stack

- **Language:** Python
- **Machine Learning:** scikit-learn / pandas / numpy
- **Backend API:** Flask
- **Database:** MongoDB
- **Visualization:** Plotly / Matplotlib (or dashboard framework of choice)

## Architecture

```
Transaction Data → Flask API → ML Pipeline
                                   ├── Preprocessing (pandas/numpy)
                                   ├── Anomaly Detection Model (scikit-learn)
                                   └── MongoDB (transaction storage & history)
                                        │
                                        ▼
                              Dashboard (spending trends, alerts, insights)
```

## Getting Started

### Prerequisites

- Python 3.10+
- MongoDB instance (local or Atlas)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/personal-finance-anomaly-detector.git
cd personal-finance-anomaly-detector

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your MongoDB URI and other config to .env
```

### Running Locally

```bash
flask run
```

The app will be available at `http://localhost:5000`.

## Usage

1. Upload or connect your transaction data (CSV import or API feed).
2. The ML pipeline preprocesses and analyzes transactions for anomalies.
3. View flagged transactions and spending trends on the dashboard.
4. Get personalized insights on unusual or risky financial behavior.

## Project Structure

```
personal-finance-anomaly-detector/
├── app/
│   ├── __init__.py
│   ├── routes/               # Flask API endpoints
│   ├── models/                # ML models (training & inference)
│   ├── services/              # Data processing & anomaly detection logic
│   └── database/              # MongoDB connection & schemas
├── dashboard/                 # Dashboard/frontend files
├── notebooks/                 # ML experimentation & model training
├── data/                       # Sample/raw transaction data (gitignored)
├── requirements.txt
├── .env.example
└── README.md
```

## Roadmap

- [ ] Bank API integration (e.g., Plaid)
- [ ] Email/SMS alerts for high-risk anomalies
- [ ] Model retraining pipeline with user feedback loop

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.


