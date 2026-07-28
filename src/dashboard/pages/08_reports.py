import plotly.express as px
import requests
import streamlit as st

from src.dashboard.utils.db import (
    get_company_id,
    get_company_names,
    get_documents,
)

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Annual Reports",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Annual Reports")
st.caption("Browse company annual reports directly from BSE.")

# ==========================================================
# Company Selection
# ==========================================================

company_name = st.selectbox(
    "Search Company",
    get_company_names(),
)

company_id = get_company_id(company_name)

reports = get_documents(company_id)

# ==========================================================
# URL Availability Checker
# ==========================================================


@st.cache_data(ttl=600)
def check_report(url):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
        )
    }

    try:

        r = requests.get(
            url,
            headers=headers,
            allow_redirects=True,
            timeout=10,
        )

        st.write(
            {
                "url": url,
                "status": r.status_code,
                "content_type": r.headers.get("Content-Type"),
            }
        )

        return r.status_code == 200

    except Exception as e:

        st.error(e)
        return False


# ==========================================================
# Dashboard Summary
# ==========================================================

left, right = st.columns(2)

with left:

    st.metric(
        "Available Report Records",
        len(reports),
    )

with right:

    if reports.empty:

        st.metric(
            "Latest Report",
            "-",
        )

    else:

        st.metric(
            "Latest Report",
            reports.iloc[0]["year"],
        )

st.divider()


# ==========================================================
# Annual Reports
# ==========================================================

st.subheader(f"📚 Annual Reports — {company_name}")

if reports.empty:

    st.warning("No annual reports available for this company.")

else:

    for _, row in reports.iterrows():

        year = str(row["year"])
        url = row["annual_report"]

        available = check_report(url)

        col1, col2, col3 = st.columns([1, 1, 4])

        with col1:

            st.markdown(f"**{year}**")

        with col2:

            if available:

                st.markdown(
                    """
                    <span style="
                        background:#16a34a;
                        color:white;
                        padding:4px 10px;
                        border-radius:12px;
                        font-size:12px;
                    ">
                    Available
                    </span>
                    """,
                    unsafe_allow_html=True,
                )

            else:

                st.markdown(
                    """
                    <span style="
                        background:#dc2626;
                        color:white;
                        padding:4px 10px;
                        border-radius:12px;
                        font-size:12px;
                    ">
                    Report Unavailable
                    </span>
                    """,
                    unsafe_allow_html=True,
                )

        with col3:

            if available:

                st.link_button(
                    f"📄 Open {year} Annual Report",
                    url,
                    use_container_width=True,
                )

            else:

                st.caption("No downloadable report available.")

        st.divider()


# ==========================================================
# Report Statistics
# ==========================================================

st.subheader("📊 Report Statistics")

if not reports.empty:

    report_status = reports.copy()

    report_status["available"] = report_status["annual_report"].apply(check_report)

    available_count = int(report_status["available"].sum())
    unavailable_count = len(report_status) - available_count

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Reports",
            len(report_status),
        )

    with col2:

        st.metric(
            "Available",
            available_count,
        )

    with col3:

        st.metric(
            "Unavailable",
            unavailable_count,
        )

    st.divider()

    # ======================================================
    # Report Timeline
    # ======================================================

    st.subheader("📈 Annual Report Timeline")

    timeline = report_status.copy()

    timeline["Status"] = timeline["available"].map(
        {
            True: "Available",
            False: "Unavailable",
        }
    )

    fig = px.scatter(
        timeline,
        x="year",
        y=["Reports"] * len(timeline),
        color="Status",
        hover_data=["year"],
        title="Annual Report Availability",
    )

    fig.update_layout(
        yaxis=dict(
            visible=False,
            showticklabels=False,
        ),
        xaxis_title="Year",
        height=250,
    )

    st.plotly_chart(
        fig,
        width="stretch",
    )

    st.divider()

# ==========================================================
# Information
# ==========================================================

with st.expander("ℹ️ About Annual Reports"):

    st.markdown("""
Annual reports are retrieved from the **BSE (Bombay Stock Exchange)**.

This page allows you to:

- Browse available annual reports
- Open the official BSE PDF
- Identify unavailable reports automatically
- View reporting history by year

Unavailable reports are detected automatically when the BSE URL
returns an HTTP **404 Not Found** response.
""")

st.divider()

st.caption("Financial Intelligence Platform • Sprint 2 • Annual Reports Dashboard")
