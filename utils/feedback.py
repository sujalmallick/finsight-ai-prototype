# components/feedback.py
import streamlit as st
from datetime import datetime

def show_feedback():
    st.header("💬 Share Your Feedback")
    feedback = st.text_area("How was your FinSight experience?")

    if st.button("Submit Feedback"):
        if feedback.strip():
            # Save feedback to a txt file
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            with open(f"feedback_{timestamp}.txt", "w", encoding="utf-8") as f:
                f.write(feedback)
            st.success("Thanks for your feedback! 🎉")
        else:
            st.warning("Please write something before submitting.")
