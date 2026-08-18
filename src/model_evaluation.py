import pandas as pd


INPUT_PATH = "outputs/anomaly_results.csv"


def evaluate_model():

    df = pd.read_csv(INPUT_PATH)

    # --------------------------------------------------
    # BASIC MODEL METRICS
    # --------------------------------------------------

    total_transactions = len(df)

    anomalies = (
        df["is_anomaly"] == 1
    ).sum()

    normal_transactions = (
        df["is_anomaly"] == 0
    ).sum()

    anomaly_percentage = (
        anomalies / total_transactions
    ) * 100

    # --------------------------------------------------
    # ANOMALY SCORE ANALYSIS
    # --------------------------------------------------

    normal_scores = df[
        df["is_anomaly"] == 0
    ]["anomaly_score"]

    anomaly_scores = df[
        df["is_anomaly"] == 1
    ]["anomaly_score"]

    # --------------------------------------------------
    # FEATURE COMPARISON
    # --------------------------------------------------

    numeric_features = [
        "amount",
        "amount_log",
        "amount_vs_category_avg",
        "day",
        "month",
        "day_of_week",
        "is_weekend"
    ]

    comparison = []

    for feature in numeric_features:

        normal_mean = (
            df[df["is_anomaly"] == 0][feature]
            .mean()
        )

        anomaly_mean = (
            df[df["is_anomaly"] == 1][feature]
            .mean()
        )

        comparison.append(
            {
                "feature": feature,
                "normal_mean": normal_mean,
                "anomaly_mean": anomaly_mean
            }
        )

    comparison_df = pd.DataFrame(
        comparison
    )

    # --------------------------------------------------
    # OUTPUT
    # --------------------------------------------------

    print("\n" + "=" * 60)
    print("ISOLATION FOREST MODEL EVALUATION")
    print("=" * 60)

    print(
        f"\nTotal Transactions : {total_transactions:,}"
    )

    print(
        f"Normal Transactions: {normal_transactions:,}"
    )

    print(
        f"Anomalies Detected : {anomalies:,}"
    )

    print(
        f"Anomaly Percentage : {anomaly_percentage:.2f}%"
    )

    print("\nAnomaly Score Statistics")
    print("-" * 40)

    print(
        f"Normal Mean Score  : "
        f"{normal_scores.mean():.6f}"
    )

    print(
        f"Anomaly Mean Score : "
        f"{anomaly_scores.mean():.6f}"
    )

    print(
        f"Normal Min Score   : "
        f"{normal_scores.min():.6f}"
    )

    print(
        f"Anomaly Min Score  : "
        f"{anomaly_scores.min():.6f}"
    )

    print("\nFeature Comparison")
    print("-" * 60)

    print(
        comparison_df.to_string(
            index=False
        )
    )


if __name__ == "__main__":

    evaluate_model()