import pandas as pd


# --------------------------------------------------
# FINANCIAL INSIGHTS
# --------------------------------------------------

def generate_insights(df, analysis_df):
    """
    Generate human-readable financial insights
    from transaction and anomaly data.
    """

    insights = []

    # --------------------------------------------------
    # BASIC CHECK
    # --------------------------------------------------

    if df.empty:
        return ["No transaction data available."]

    # --------------------------------------------------
    # HIGHEST SPENDING CATEGORY
    # --------------------------------------------------

    category_spending = (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    highest_category = category_spending.index[0]
    highest_category_amount = category_spending.iloc[0]

    insights.append(
        f"Your highest spending category is "
        f"{highest_category}, with total spending of "
        f"₹{highest_category_amount:,.2f}."
    )

    # --------------------------------------------------
    # HIGHEST SPENDING MERCHANT
    # --------------------------------------------------

    merchant_spending = (
        df.groupby("merchant")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    highest_merchant = merchant_spending.index[0]
    highest_merchant_amount = merchant_spending.iloc[0]

    insights.append(
        f"Your highest spending merchant is "
        f"{highest_merchant}, with total spending of "
        f"₹{highest_merchant_amount:,.2f}."
    )

    # --------------------------------------------------
    # AVERAGE TRANSACTION
    # --------------------------------------------------

    average_transaction = df["amount"].mean()

    insights.append(
        f"Your average transaction amount is "
        f"₹{average_transaction:,.2f}."
    )

    # --------------------------------------------------
    # ANOMALY INSIGHTS
    # --------------------------------------------------

    anomalies = analysis_df[
        analysis_df["is_anomaly"] == 1
    ].copy()

    if not anomalies.empty:

        # Largest anomaly
        largest_anomaly = anomalies.loc[
            anomalies["amount"].idxmax()
        ]

        insights.append(
            f"The largest detected anomaly is "
            f"Transaction {int(largest_anomaly['transaction_id'])}, "
            f"with an amount of "
            f"₹{largest_anomaly['amount']:,.2f}."
        )

        # High-risk anomalies
        high_risk_count = (
            anomalies["severity"] == "High"
        ).sum()

        insights.append(
            f"There are {high_risk_count} high-risk "
            f"transactions among the detected anomalies."
        )

        # Weekend anomalies
        weekend_anomalies = (
            anomalies["is_weekend"] == 1
        ).sum()

        weekend_percentage = (
            weekend_anomalies / len(anomalies)
        ) * 100

        insights.append(
            f"{weekend_percentage:.1f}% of detected anomalies "
            f"occurred on weekends."
        )

        # Category with most anomalies
        anomaly_categories = (
            anomalies["category"]
            .value_counts()
        )

        top_anomaly_category = (
            anomaly_categories.index[0]
        )

        top_anomaly_category_count = (
            anomaly_categories.iloc[0]
        )

        insights.append(
            f"{top_anomaly_category} has the highest number "
            f"of detected anomalies, with "
            f"{top_anomaly_category_count} transactions."
        )

    else:

        insights.append(
            "No anomalies were detected in the selected data."
        )

    return insights


# --------------------------------------------------
# TEST MODULE
# --------------------------------------------------

if __name__ == "__main__":

    DATA_PATH = "outputs/anomaly_results.csv"
    ANALYSIS_PATH = "outputs/anomaly_analysis.csv"

    df = pd.read_csv(DATA_PATH)
    analysis_df = pd.read_csv(ANALYSIS_PATH)

    insights = generate_insights(
        df,
        analysis_df
    )

    print("\nFinancial Insights:")
    print("-" * 60)

    for i, insight in enumerate(
        insights,
        start=1
    ):
        print(f"{i}. {insight}")