import streamlit as st 
st.set_page_config(page_title="FinSight AI 💸", layout="wide")

import pandas as pd
from utils.pdf_parser import extract_text_from_pdf
from utils.transaction_parser import parse_transactions
from utils.categorizer import categorize_bulk  # ✅ BULK GPT Categorizer
from components.dashboard import explain_spending
from utils.feedback import show_feedback

def main():
    st.title("📂 Upload Your Statement")

    uploaded_file = st.file_uploader("Upload PDF statement", type=["pdf"])

    if uploaded_file:
        # 📄 Step 1: Extract raw text from PDF
        text = extract_text_from_pdf(uploaded_file)

        # 🔍 Step 2: Parse to raw transactions
        transactions = parse_transactions(text)

        # 🔮 Step 3: AI Categorize in bulk
        categorized_transactions = categorize_bulk(transactions)

        # 🧾 Step 4: Convert to DataFrame
        df = pd.DataFrame(categorized_transactions)

        # ✅ Step 5: Show categorized preview
        st.subheader("🧠 Categorized Transactions Preview")
        st.write(df.head())

        # 📊 Step 6: Visual Insights
        explain_spending(categorized_transactions)

        # 📝 Step 7: User feedback
        show_feedback()

if __name__ == "__main__":
    main()
