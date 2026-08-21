# MAIN APPLICATION

import streamlit as st
import pandas as pd
import plotly.express as px
from src.financial_insights import generate_insights
from src.ai_assistant import ask_financial_assistant

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Personal Finance Anomaly Detector",
    page_icon="💰",
    layout="wide"
)
st.markdown(
    """
    <style>
    .chart-box {
        border: 1px solid rgba(128, 128, 128, 0.35);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        background-color: rgba(128, 128, 128, 0.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

DATA_PATH = "outputs/anomaly_results.csv"
ANALYSIS_PATH = "outputs/anomaly_analysis.csv"

df = pd.read_csv(DATA_PATH)
analysis_df = pd.read_csv(ANALYSIS_PATH)

df["date"] = pd.to_datetime(df["date"])
analysis_df["date"] = pd.to_datetime(analysis_df["date"])


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown(
    """
    <div style="text-align: center;">
        <h1>💰 Personal Finance Anomaly Detector</h1>
        <p style="font-size: 20px;">
            AI-powered financial transaction analysis and anomaly detection
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

# --------------------------------------------------
# FILTERS
# --------------------------------------------------

st.subheader("🔎 Filters")

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

min_date = df["date"].min().date()
max_date = df["date"].max().date()

categories = sorted(df["category"].unique())

payment_methods = sorted(df["payment_method"].unique())


with filter_col1:

    st.markdown(
        "<div style='text-align:center; font-weight:bold;'>Date Range</div>",
        unsafe_allow_html=True
    )

    date_range = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )


with filter_col2:

    st.markdown(
        "<div style='text-align:center; font-weight:bold;'>Category</div>",
        unsafe_allow_html=True
    )

    selected_categories = st.multiselect(
        "Category",
        categories,
        default=categories,
        label_visibility="collapsed"
    )


with filter_col3:

    st.markdown(
        "<div style='text-align:center; font-weight:bold;'>Payment Method</div>",
        unsafe_allow_html=True
    )

    selected_payment_methods = st.multiselect(
        "Payment Method",
        payment_methods,
        default=payment_methods,
        label_visibility="collapsed"
    )


with filter_col4:

    st.markdown(
        "<div style='text-align:center; font-weight:bold;'>Transaction Type</div>",
        unsafe_allow_html=True
    )

    transaction_type = st.selectbox(
        "Transaction Type",
        [
            "All Transactions",
            "Normal Transactions",
            "Anomalies Only"
        ],
        label_visibility="collapsed"
    )


# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df.copy()


if len(date_range) == 2:

    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1]) + pd.Timedelta(days=1)

    filtered_df = filtered_df[
        (filtered_df["date"] >= start_date)
        & (filtered_df["date"] < end_date)
    ]


filtered_df = filtered_df[
    filtered_df["category"].isin(
        selected_categories
    )
]


filtered_df = filtered_df[
    filtered_df["payment_method"].isin(
        selected_payment_methods
    )
]


if transaction_type == "Normal Transactions":

    filtered_df = filtered_df[
        filtered_df["is_anomaly"] == 0
    ]

elif transaction_type == "Anomalies Only":

    filtered_df = filtered_df[
        filtered_df["is_anomaly"] == 1
    ]


# --------------------------------------------------
# MERGE ANALYSIS DATA
# --------------------------------------------------

filtered_analysis = analysis_df[
    [
        "transaction_id",
        "amount_difference",
        "amount_difference_percent",
        "reason",
        "severity",
        "risk_score"
    ]
]


filtered_df = filtered_df.merge(
    filtered_analysis,
    on="transaction_id",
    how="left"
)


# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_transactions = len(filtered_df)

total_spending = filtered_df["amount"].sum()

anomalies = (
    filtered_df["is_anomaly"] == 1
).sum()

high_risk = (
    filtered_df["severity"] == "High"
).sum()
average_risk_score = (
    filtered_df["risk_score"].mean()
    if len(filtered_df) > 0
    else 0
)

if total_transactions > 0:

    anomaly_percentage = (
        anomalies / total_transactions
    ) * 100

else:

    anomaly_percentage = 0

# --------------------------------------------------
# AI FINANCIAL CONTEXT
# --------------------------------------------------

if len(filtered_df) > 0:

    category_spending = (
        filtered_df
        .groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    top_category = category_spending.index[0]
    top_category_amount = category_spending.iloc[0]

    merchant_spending = (
        filtered_df
        .groupby("merchant")["amount"]
        .sum()
        .sort_values(ascending=False)
    )

    top_merchant = merchant_spending.index[0]
    top_merchant_amount = merchant_spending.iloc[0]

    high_risk_count = (
        filtered_df["severity"] == "High"
    ).sum()

    top_suspicious = (
        filtered_df[
            filtered_df["is_anomaly"] == 1
        ]
        .sort_values(
            "risk_score",
            ascending=False
        )
        .head(5)
    )

    suspicious_transactions = ""

    for _, row in top_suspicious.iterrows():

        suspicious_transactions += f"""
Transaction ID: {int(row['transaction_id'])}
Date: {row['date'].date()}
Category: {row['category']}
Merchant: {row['merchant']}
Amount: ₹{row['amount']:,.2f}
Payment Method: {row['payment_method']}
Risk Score: {row['risk_score']:.0f}/100
Severity: {row['severity']}
Reason: {row['reason']}
Amount Difference: {row['amount_difference_percent']:.2f}%

"""
    average_transaction = (
        filtered_df["amount"].mean()
    )

    financial_context = f"""
Total transactions: {total_transactions}
Total spending: ₹{total_spending:,.2f}
Anomalies detected: {anomalies}
Anomaly percentage: {anomaly_percentage:.2f}%
High-risk anomalies: {high_risk_count}
Average transaction amount: ₹{average_transaction:,.2f}

Highest spending category:
{top_category} — ₹{top_category_amount:,.2f}

Highest spending merchant:
{top_merchant} — ₹{top_merchant_amount:,.2f}

Transaction type filter:
{transaction_type}

Selected categories:
{", ".join(selected_categories)}

Selected payment methods:
{", ".join(selected_payment_methods)}

TOP 5 SUSPICIOUS TRANSACTIONS:

{suspicious_transactions}
"""


else:

    financial_context = """
No transactions were found for the selected filters.
"""
# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "Total Transactions",
        f"{total_transactions:,}"
    )


with col2:

    st.metric(
        "Total Spending",
        f"₹{total_spending:,.2f}"
    )


with col3:

    st.metric(
        "Anomalies Detected",
        f"{anomalies:,}"
    )


with col4:

    st.metric(
        "High Risk",
        f"{high_risk:,}"
    )

with col5:

    st.metric(
        "Avg Risk Score",
        f"{average_risk_score:.1f}/100"
    )

st.divider()

# --------------------------------------------------
# FINANCIAL INSIGHTS
# --------------------------------------------------

st.markdown(
    """
    <h2 style="text-align: center;">Financial Insights</h2>
    """,
    unsafe_allow_html=True
)


insight_analysis_df = filtered_df[
    filtered_df["is_anomaly"] == 1
].copy()


insights = generate_insights(
    filtered_df,
    insight_analysis_df
)


for insight in insights:

    st.info(insight)


st.divider()
# --------------------------------------------------
# SPENDING OVER TIME
# --------------------------------------------------

st.markdown(
    """
    <h2 style="text-align: center;">Spending Over Time</h2>
    """,
    unsafe_allow_html=True
)


daily_spending = (
    filtered_df
    .groupby(
        filtered_df["date"].dt.date
    )["amount"]
    .sum()
    .reset_index()
)

daily_spending.columns = [
    "date",
    "amount"
]

fig_time = px.line(
    daily_spending,
    x="date",
    y="amount",
    title="Daily Spending Trend",
    labels={
        "date": "Date",
        "amount": "Amount (₹)"
    }
)

fig_time.update_layout(
    title_x=0.5,
    margin=dict(t=50, l=20, r=20, b=20)
)

st.markdown('<div class="chart-box">', unsafe_allow_html=True)

with st.container(border=True):
    st.plotly_chart(
        fig_time,
        use_container_width=True
    )

st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# CATEGORY ANALYSIS
# --------------------------------------------------

col1, col2 = st.columns(2)


with col1:

    st.subheader("📊 Spending by Category")

    category_spending = (
        filtered_df
        .groupby("category")["amount"]
        .sum()
        .reset_index()
        .sort_values(
            "amount",
            ascending=False
        )
    )

    fig_category = px.bar(
        category_spending,
        x="category",
        y="amount",
        title="Total Spending by Category",
        labels={
            "category": "Category",
            "amount": "Amount (₹)"
        }
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


with col2:

    st.subheader("🚨 Anomalies by Category")

    category_anomalies = (
        filtered_df[
            filtered_df["is_anomaly"] == 1
        ]
        .groupby("category")
        .size()
        .reset_index(
            name="anomalies"
        )
        .sort_values(
            "anomalies",
            ascending=False
        )
    )

    fig_anomaly_category = px.bar(
        category_anomalies,
        x="category",
        y="anomalies",
        title="Detected Anomalies by Category",
        labels={
            "category": "Category",
            "anomalies": "Number of Anomalies"
        }
    )

    st.plotly_chart(
        fig_anomaly_category,
        use_container_width=True
    )


# --------------------------------------------------
# SEVERITY ANALYSIS
# --------------------------------------------------

st.subheader("⚠️ Anomaly Severity")


severity_df = (
    filtered_df[
        filtered_df["is_anomaly"] == 1
    ]["severity"]
    .value_counts()
    .reset_index()
)


severity_df.columns = [
    "severity",
    "count"
]


fig_severity = px.bar(
    severity_df,
    x="severity",
    y="count",
    title="Anomalies by Severity",
    labels={
        "severity": "Severity",
        "count": "Number of Anomalies"
    }
)


st.plotly_chart(
    fig_severity,
    use_container_width=True
)


# --------------------------------------------------
# PAYMENT METHOD ANALYSIS
# --------------------------------------------------

st.subheader("💳 Payment Method Analysis")


payment_analysis = (
    filtered_df
    .groupby("payment_method")
    .agg(
        transactions=("transaction_id", "count"),
        spending=("amount", "sum"),
        anomalies=("is_anomaly", "sum")
    )
    .reset_index()
)


fig_payment = px.bar(
    payment_analysis,
    x="payment_method",
    y="anomalies",
    title="Anomalies by Payment Method",
    labels={
        "payment_method": "Payment Method",
        "anomalies": "Anomalies"
    }
)


st.plotly_chart(
    fig_payment,
    use_container_width=True
)


# --------------------------------------------------
# NORMAL VS ANOMALOUS
# --------------------------------------------------

st.subheader("🚨 Transaction Classification")


classification = (
    filtered_df["is_anomaly"]
    .map({
        0: "Normal",
        1: "Anomaly"
    })
    .value_counts()
    .reset_index()
)


classification.columns = [
    "Type",
    "Count"
]


fig_classification = px.pie(
    classification,
    names="Type",
    values="Count",
    title="Normal vs Anomalous Transactions"
)


st.plotly_chart(
    fig_classification,
    use_container_width=True
)
# --------------------------------------------------
# ML MODEL EVALUATION
# --------------------------------------------------

st.subheader("🤖 ML Model Evaluation")


# --------------------------------------------------
# MODEL METRICS
# --------------------------------------------------

normal_transactions = (
    filtered_df["is_anomaly"] == 0
).sum()

anomalous_transactions = (
    filtered_df["is_anomaly"] == 1
).sum()


if len(filtered_df) > 0:

    filtered_anomaly_rate = (
        anomalous_transactions /
        len(filtered_df)
    ) * 100

else:

    filtered_anomaly_rate = 0


normal_scores = filtered_df[
    filtered_df["is_anomaly"] == 0
]["anomaly_score"]


anomaly_scores = filtered_df[
    filtered_df["is_anomaly"] == 1
]["anomaly_score"]


if len(normal_scores) > 0:

    normal_mean_score = normal_scores.mean()

else:

    normal_mean_score = 0


if len(anomaly_scores) > 0:

    anomaly_mean_score = anomaly_scores.mean()

else:

    anomaly_mean_score = 0


# --------------------------------------------------
# METRIC CARDS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Normal Transactions",
        f"{normal_transactions:,}"
    )


with col2:

    st.metric(
        "Anomalous Transactions",
        f"{anomalous_transactions:,}"
    )


with col3:

    st.metric(
        "Anomaly Rate",
        f"{filtered_anomaly_rate:.2f}%"
    )


with col4:

    st.metric(
        "Anomaly Score Gap",
        f"{normal_mean_score - anomaly_mean_score:.4f}"
    )


# --------------------------------------------------
# ANOMALY SCORE DISTRIBUTION
# --------------------------------------------------

score_df = pd.DataFrame(
    {
        "Anomaly Score": pd.concat(
            [
                normal_scores,
                anomaly_scores
            ],
            ignore_index=True
        ),
        "Transaction Type": (
            ["Normal"] * len(normal_scores)
            +
            ["Anomaly"] * len(anomaly_scores)
        )
    }
)


if not score_df.empty:

    fig_score = px.histogram(
        score_df,
        x="Anomaly Score",
        color="Transaction Type",
        nbins=40,
        title="Isolation Forest Anomaly Score Distribution",
        labels={
            "Anomaly Score": "Anomaly Score",
            "count": "Number of Transactions"
        }
    )

    fig_score.add_vline(
        x=0,
        line_dash="dash",
        annotation_text="Anomaly Boundary"
    )

    st.plotly_chart(
        fig_score,
        use_container_width=True
    )

# --------------------------------------------------
# FEATURE BEHAVIOR ANALYSIS
# --------------------------------------------------

st.subheader("📊 Anomalous Transaction Behavior")


# --------------------------------------------------
# WEEKEND BEHAVIOR
# --------------------------------------------------

weekend_comparison = (
    filtered_df
    .groupby("is_anomaly")["is_weekend"]
    .mean()
    .reset_index()
)


weekend_comparison["Transaction Type"] = (
    weekend_comparison["is_anomaly"]
    .map({
        0: "Normal",
        1: "Anomaly"
    })
)


weekend_comparison["Weekend Percentage"] = (
    weekend_comparison["is_weekend"] * 100
)


fig_weekend = px.bar(
    weekend_comparison,
    x="Transaction Type",
    y="Weekend Percentage",
    title="Weekend Transaction Comparison",
    labels={
        "Weekend Percentage": "Weekend Transactions (%)",
        "Transaction Type": "Transaction Type"
    },
    text="Weekend Percentage"
)


fig_weekend.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)


st.plotly_chart(
    fig_weekend,
    use_container_width=True
)
# --------------------------------------------------
# TRANSACTION AMOUNT BEHAVIOR
# --------------------------------------------------

amount_comparison = (
    filtered_df
    .groupby("is_anomaly")["amount"]
    .mean()
    .reset_index()
)


amount_comparison["Transaction Type"] = (
    amount_comparison["is_anomaly"]
    .map({
        0: "Normal",
        1: "Anomaly"
    })
)


fig_amount = px.bar(
    amount_comparison,
    x="Transaction Type",
    y="amount",
    title="Average Transaction Amount",
    labels={
        "amount": "Average Amount (₹)",
        "Transaction Type": "Transaction Type"
    },
    text="amount"
)


fig_amount.update_traces(
    texttemplate="₹%{text:,.2f}",
    textposition="outside"
)


st.plotly_chart(
    fig_amount,
    use_container_width=True
)
# --------------------------------------------------
# MODEL INTERPRETATION
# --------------------------------------------------

st.info(
    "Isolation Forest identifies unusual transactions "
    "by assigning lower anomaly scores to observations "
    "that are easier to isolate from the normal transaction "
    "patterns."
)


st.divider()

# --------------------------------------------------
# DETECTED ANOMALIES
# --------------------------------------------------

st.subheader("🔴 Detected Anomalies")


filtered_anomalies = filtered_df[
    filtered_df["is_anomaly"] == 1
].copy()


display_columns = [
    "transaction_id",
    "date",
    "category",
    "merchant",
    "amount",
    "payment_method",
    "anomaly_score",
    "risk_score",
    "severity",
    "amount_difference_percent",
    "reason"
]

if len(filtered_anomalies) > 0:

    filtered_anomalies = (
    filtered_anomalies
    .sort_values(
        "risk_score",
        ascending=False
    )
)

    st.dataframe(
        filtered_anomalies[
            display_columns
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "No anomalies found for the selected filters."
    )


# --------------------------------------------------
# MOST SUSPICIOUS TRANSACTIONS
# --------------------------------------------------

st.subheader("🚨 Most Suspicious Transactions")


top_anomalies = filtered_anomalies.head(5)


for _, row in top_anomalies.iterrows():

    with st.expander(
        f"Transaction {int(row['transaction_id'])} — "
f"₹{row['amount']:,.2f} — "
f"Risk {row['risk_score']:.0f}/100 — "
f"{row['severity']}"
    ):

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Category:** {row['category']}"
            )

            st.write(
                f"**Merchant:** {row['merchant']}"
            )

            st.write(
                f"**Payment Method:** "
                f"{row['payment_method']}"
            )

        with col2:

            st.write(
                f"**Anomaly Score:** "
                f"{row['anomaly_score']:.6f}"
            )

            st.write(
                f"**Risk Score:** "
                f"{row['risk_score']:.0f}/100"
            )

            st.write(
                f"**Severity:** "
                f"{row['severity']}"
            )

            st.write(
                f"**Amount Difference:** "
            f"{row['amount_difference_percent']:.2f}%"
    )
# --------------------------------------------------
# AI FINANCIAL ASSISTANT
# --------------------------------------------------

# --------------------------------------------------
# AI FINANCIAL ASSISTANT
# --------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.divider()

st.subheader("🤖 AI Financial Assistant")

st.write(
    "Ask questions about your spending, anomalies, "
    "categories, merchants, and risk patterns."
)

# Display previous conversation
for chat in st.session_state.chat_history:

    with st.chat_message("user"):
        st.markdown(chat["question"])

    with st.chat_message("assistant"):
        st.markdown(chat["answer"])


# ChatGPT-style input
question = st.chat_input(
    "Ask your financial question..."
)

if question:

    # Display user's new message immediately
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner(
            "Gemini is analyzing your financial data..."
        ):

            try:

                conversation_context = ""

                for chat in st.session_state.chat_history:

                    conversation_context += f"""
Previous User Question:
{chat['question']}

Previous Gemini Answer:
{chat['answer']}

"""

                combined_context = f"""
{financial_context}

CONVERSATION HISTORY:

{conversation_context}
"""

                answer = ask_financial_assistant(
                    question,
                    combined_context
                )

                st.markdown(answer)

                st.session_state.chat_history.append(
                    {
                        "question": question,
                        "answer": answer
                    }
                )

            except Exception as e:

                st.error(
                    f"Unable to get a response from Gemini: {e}"
                )
# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

if st.session_state.chat_history:

    st.subheader("💬 Conversation")

    for chat in st.session_state.chat_history:

        with st.chat_message("user"):
            st.markdown(chat["question"])

        with st.chat_message("assistant"):
            st.markdown(chat["answer"])

        st.divider()
# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Personal Finance Anomaly Detector | "
    "Machine Learning powered by Isolation Forest"
)
