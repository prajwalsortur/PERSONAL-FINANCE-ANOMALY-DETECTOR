import pandas as pd
import matplotlib.pyplot as plt


INPUT_PATH = "outputs/anomaly_results.csv"
OUTPUT_PATH = "outputs/anomaly_score_distribution.png"


def create_visualization():

    df = pd.read_csv(INPUT_PATH)

    normal_scores = df[
        df["is_anomaly"] == 0
    ]["anomaly_score"]

    anomaly_scores = df[
        df["is_anomaly"] == 1
    ]["anomaly_score"]

    # --------------------------------------------------
    # ANOMALY SCORE DISTRIBUTION
    # --------------------------------------------------

    plt.figure(figsize=(10, 6))

    plt.hist(
        normal_scores,
        bins=40,
        alpha=0.7,
        label="Normal Transactions"
    )

    plt.hist(
        anomaly_scores,
        bins=40,
        alpha=0.7,
        label="Anomalous Transactions"
    )

    plt.axvline(
        0,
        linestyle="--",
        label="Anomaly Boundary"
    )

    plt.xlabel("Anomaly Score")
    plt.ylabel("Number of Transactions")

    plt.title(
        "Isolation Forest Anomaly Score Distribution"
    )

    plt.legend()

    plt.tight_layout()

    plt.savefig(
        OUTPUT_PATH,
        dpi=300
    )

    plt.close()

    print(
        f"Visualization saved to: {OUTPUT_PATH}"
    )


if __name__ == "__main__":

    create_visualization()