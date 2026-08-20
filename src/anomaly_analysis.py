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
    # RISK SCORE
    # --------------------------------------------------

    def calculate_risk_score(row):

        score = 0

        # ----------------------------------------------
        # ISOLATION FOREST SCORE
        # ----------------------------------------------

        anomaly_score = row["anomaly_score"]

        # More negative = more suspicious
        if anomaly_score <= -0.05:
            score += 50

        elif anomaly_score <= -0.03:
            score += 40

        elif anomaly_score <= -0.01:
            score += 30

        else:
            score += 20

        # ----------------------------------------------
        # CATEGORY AMOUNT DIFFERENCE
        # ----------------------------------------------

        amount_ratio = row["amount_vs_category_avg"]

        if amount_ratio >= 5:
            score += 35

        elif amount_ratio >= 3:
            score += 30

        elif amount_ratio >= 2:
            score += 20

        elif amount_ratio >= 1.5:
            score += 10

        elif amount_ratio <= 0.1:
            score += 25

        elif amount_ratio <= 0.5:
            score += 15

        # ----------------------------------------------
        # EXTREMELY HIGH TRANSACTION
        # ----------------------------------------------

        if row["amount"] >= high_amount_threshold:
            score += 10

        # ----------------------------------------------
        # WEEKEND
        # ----------------------------------------------

        if row["is_weekend"] == 1:
            score += 5

        # Maximum score = 100
        return min(score, 100)

    anomalies["risk_score"] = anomalies.apply(
        calculate_risk_score,
        axis=1
    )

    # --------------------------------------------------
    # GENERATE REASONS
    # --------------------------------------------------

    def generate_reason(row):

        reasons = []

        amount = row["amount"]
        category_average = row["category_avg_amount"]
        amount_ratio = row["amount_vs_category_avg"]

        # ----------------------------------------------
        # HIGHER THAN CATEGORY AVERAGE
        # ----------------------------------------------

        if amount_ratio >= 2:

            percentage = (
                (amount_ratio - 1) * 100
            )

            reasons.append(
                f"Amount is {percentage:.1f}% above the "
                f"category average "
                f"(₹{amount:,.2f} vs "
                f"₹{category_average:,.2f})"
            )

        elif amount_ratio >= 1.5:

            percentage = (
                (amount_ratio - 1) * 100
            )

            reasons.append(
                f"Amount is {percentage:.1f}% above the "
                f"category average "
                f"(₹{amount:,.2f} vs "
                f"₹{category_average:,.2f})"
            )

        # ----------------------------------------------
        # LOWER THAN CATEGORY AVERAGE
        # ----------------------------------------------

        elif amount_ratio <= 0.5:

            percentage = (
                (1 - amount_ratio) * 100
            )

            reasons.append(
                f"Amount is {percentage:.1f}% below the "
                f"category average "
                f"(₹{amount:,.2f} vs "
                f"₹{category_average:,.2f})"
            )

        # ----------------------------------------------
        # EXTREMELY HIGH TRANSACTION
        # ----------------------------------------------

        if amount >= high_amount_threshold:

            reasons.append(
                "Transaction amount is unusually high"
            )

        # ----------------------------------------------
        # WEEKEND
        # ----------------------------------------------

        if row["is_weekend"] == 1:

            reasons.append(
                "Transaction occurred on a weekend"
            )

        # ----------------------------------------------
        # FALLBACK
        # ----------------------------------------------

        if not reasons:

            reasons.append(
                "Transaction pattern differs from "
                "normal transactions"
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

        risk_score = row["risk_score"]

        if risk_score >= 80:
            return "High"

        elif risk_score >= 50:
            return "Medium"

        else:
            return "Low"

    anomalies["severity"] = anomalies.apply(
        calculate_severity,
        axis=1
    )

    # --------------------------------------------------
    # SORT BY RISK
    # --------------------------------------------------

    anomalies = anomalies.sort_values(
        by="risk_score",
        ascending=False
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

    print("\nRisk score statistics:")

    print(
        anomalies["risk_score"]
        .describe()
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
                "risk_score",
                "severity",
                "reason"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )


if __name__ == "__main__":

    analyze_anomalies()