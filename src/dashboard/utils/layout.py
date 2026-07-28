import streamlit as st


def configure_page(title: str):
    """
    Configure page title only.
    Page config is handled in app.py.
    """

    inject_css()

    st.title(title)


def inject_css():
    st.markdown(
        """
        <style>

        .block-container{
            padding-top:1rem;
            padding-bottom:2rem;
            padding-left:2rem;
            padding-right:2rem;
        }

        div[data-testid="metric-container"]{
            border-radius:10px;
            border:1px solid #E5E5E5;
            padding:15px;
        }

        footer{
            visibility:hidden;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def sidebar():
    st.sidebar.title("📈 Nifty 100 Analytics")

    st.sidebar.markdown("---")

    st.sidebar.success("Sprint 4 Dashboard")

    st.sidebar.markdown("""
Financial Intelligence Platform

Built with:

- Streamlit
- SQLite
- Plotly
- Pandas
""")

    st.sidebar.markdown("---")
