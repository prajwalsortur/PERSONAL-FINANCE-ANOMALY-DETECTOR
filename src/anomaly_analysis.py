import pandas as pd


INPUT_PATH = "outputs/anomaly_results.csv"
OUTPUT_PATH = "outputs/anomaly_analysis.csv"


def analyze_anomalies():

    df = pd.read_csv(INPUT_PATH)

    # Select only anomalous transactions
    anomalies = df[df["is_anomaly"] == 1].copy()

    # --------------------------------------------------
    # AMOUNT DIFFERENCE
    # --------------------------------------------------

    anomalies["amount_difference"] = (
        anomalies["amount"]
        - anomalies["category_avg_amount"]
    )

    anomalies["amount_difference_percent"] = (
        anomalies["amount_difference"]
        / anomalies["category_avg_amount"]
    ) * 100

    # --------------------------------------------------
    # HIGH AMOUNT THRESHOLD
    # --------------------------------------------------

    high_amount_threshold = df["amount"].quantile(0.95)

    # --------------------------------------------------
    # GENERATE REASONS
    # --------------------------------------------------

    def generate_reason(row):

        reasons = []

        # Amount significantly higher than category average
        if row["amount_vs_category_avg"] >= 2:
            reasons.append(
                "Amount is significantly higher than the category average"
            )

        elif row["amount_vs_category_avg"] >= 1.5:
            reasons.append(
                "Amount is higher than the category average"
            )

        # Amount significantly lower than category average
        elif row["amount_vs_category_avg"] <= 0.5:
            reasons.append(
                "Amount is significantly lower than the category average"
            )

        # Extremely high transaction
        if row["amount"] >= high_amount_threshold:
            reasons.append(
                "Transaction amount is unusually high"
            )

        # Weekend transaction
        if row["is_weekend"] == 1:
            reasons.append(
                "Transaction occurred on a weekend"
            )

        # Fallback explanation
        if not reasons:
            reasons.append(
                "Transaction pattern differs from normal transactions"
            )

        return "; ".join(reasons)

    anomalies["reason"] = anomalies.apply(
        generate_reason,
        axis=1
    )

    # --------------------------------------------------
    # SEVERITY
    # --------------------------------------------------

    def calculate_severity(row):

        score = row["anomaly_score"]
        amount_ratio = row["amount_vs_category_avg"]

        # Very suspicious
        if score < -0.05 or amount_ratio >= 3:
            return "High"

        # Moderately suspicious
        elif score < 0 or amount_ratio >= 2:
            return "Medium"

        # Less suspicious
        else:
            return "Low"

    anomalies["severity"] = anomalies.apply(
        calculate_severity,
        axis=1
    )

    # --------------------------------------------------
    # SORT BY SUSPICIOUSNESS
    # --------------------------------------------------

    anomalies = anomalies.sort_values(
        by="anomaly_score",
        ascending=True
    )

    # --------------------------------------------------
    # SAVE RESULTS
    # --------------------------------------------------

    anomalies.to_csv(
        OUTPUT_PATH,
        index=False
    )

    # --------------------------------------------------
    # OUTPUT
    # --------------------------------------------------

    print("Anomaly analysis completed successfully.")
    print(
        f"Total anomalies analyzed: {len(anomalies)}"
    )

    print(
        f"Analysis saved to: {OUTPUT_PATH}"
    )

    print("\nSeverity distribution:")

    print(
        anomalies["severity"]
        .value_counts()
    )

    print("\nTop 10 suspicious transactions:")

    print(
        anomalies[
            [
                "transaction_id",
                "category",
                "merchant",
                "amount",
                "anomaly_score",
                "severity",
                "reason"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":
    analyze_anomalies()