import streamlit as st  # Streamlit for building web UI
import altair as alt
import pandas as pd

def explain_spending(transactions):
    # Dictionary to keep total amount spent in each category
    category_totals = {}

    for i, txn in enumerate(transactions):
        # Sanity check: Skip if item is not a dictionary
        if not isinstance(txn, dict):
            st.warning(f"⚠️ Skipping item at index {i} because it's not a dict: {txn}")
            continue

        # Get transaction type (DEBIT or CREDIT)
        txn_type = txn.get("type", None)
        if txn_type is None:
            st.warning(f"⚠️ Skipping item at index {i} - missing 'type' key: {txn}")
            continue

        # Only process DEBIT transactions (i.e., spending)
        if txn_type == "DEBIT":
            category = txn.get("category", "Other")  # Default to 'Other' if missing
            amount = txn.get("amount", 0)  # Default amount = 0

            # Convert amount to float if it's a string
            if isinstance(amount, str):
                try:
                    amount = float(amount)
                except ValueError:
                    st.warning(f"⚠️ Invalid amount at index {i}: {amount}")
                    continue

            # Accumulate the total per category
            category_totals[category] = category_totals.get(category, 0) + amount

    # If no DEBIT transactions were processed
    if not category_totals:
        st.info("No valid DEBIT transactions found.")
        return

    # Sort categories by total spend (descending)
    sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)

    # Create DataFrame for chart
    df = pd.DataFrame(sorted_categories, columns=["Category", "Amount"])  # ✅ Fix added here

    # Header for the insights section
    st.markdown("### 💬 FinSight AI's Breakdown:")

    # Show the top spending category
    top_category, top_amount = sorted_categories[0]
    st.write(f"🤑 You spent the most on **{top_category}** → ₹{top_amount:.2f}")

    # Show second top category if available
    if len(sorted_categories) > 1:
        second_category, second_amount = sorted_categories[1]
        st.write(f"💸 Second most? **{second_category}** → ₹{second_amount:.2f}")

    # Show remaining categories
    if len(sorted_categories) > 2:
        st.write("📊 Other categories that hurt your wallet:")
        for cat, amt in sorted_categories[2:]:
            st.markdown(f"- **{cat}**: ₹{amt:.2f}")

    # Show chart of spending by category
    st.markdown("### 📈 Spending Overview Chart")
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("Category:N", sort="-y"),
        y="Amount:Q",
        tooltip=["Category", "Amount"]
    ).properties(
        width=600,
        height=400
    )
    st.altair_chart(chart, use_container_width=True)

    # Closing message — time for some budgeting!
    st.success("That’s the tea ☕ — time to budget smarter?")
