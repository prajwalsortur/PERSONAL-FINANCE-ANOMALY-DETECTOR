# Personal Finance Anomaly Detector


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


