import os
from dotenv import load_dotenv
from google import genai


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# --------------------------------------------------
# GEMINI CLIENT
# --------------------------------------------------

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. "
        "Please add it to the .env file."
    )

client = genai.Client(api_key=GEMINI_API_KEY)


# --------------------------------------------------
# AI FINANCIAL ASSISTANT
# --------------------------------------------------

def ask_financial_assistant(question, financial_context):
    """
    Ask Gemini a question about the user's
    financial transaction data.
    """

    prompt = f"""
You are an AI financial analysis assistant.

Analyze the financial data provided below and answer
the user's question clearly and concisely.

IMPORTANT RULES:
- Only use information provided in the financial context.
- Do not invent transactions, amounts, categories, or statistics.
- If the data does not contain enough information, say so.
- Do not provide investment or financial advice.
- Explain calculations when useful.
- Use Indian Rupees (₹) for monetary values.

FINANCIAL CONTEXT:

{financial_context}

USER QUESTION:

{question}

Give a helpful answer based only on the provided data.
"""

    response = client.models.generate_content(
       model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    test_context = """
    Total transactions: 10000
    Total spending: ₹25802174.77
    Anomalies detected: 300
    High-risk anomalies: 20
    Average transaction: ₹2580.22
    Highest spending category: Entertainment
    Highest spending merchant: Local Store
    """

    question = (
        "What is my highest spending category "
        "and how much did I spend overall?"
    )

    answer = ask_financial_assistant(
        question,
        test_context
    )

    print("\nAI Financial Assistant:")
    print("-" * 60)
    print(answer)