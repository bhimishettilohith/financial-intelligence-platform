"""
Nifty 100 Analytics Dashboard

Sprint 4 - Day 23
"""

import streamlit as st

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📈 Nifty 100 Analytics")

st.markdown(
    """
Welcome to the **Nifty 100 Analytics Dashboard**.

Use the navigation menu in the left sidebar to explore:

- 🏠 Home
- 🏢 Company Profile
- 🔍 Screener
- 👥 Peer Comparison
- 📈 Financial Trends
- 🏭 Sector Analysis
- 💰 Capital Allocation
- 📄 Reports
"""
)

st.info("Select a page from the sidebar to begin.")