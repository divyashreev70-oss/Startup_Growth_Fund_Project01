import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.insights import executive_summary

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Startup Analytics Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>
.main-header {
    font-size: 40px;
    font-weight: bold;
    color: #4F46E5;
}

.sub-header {
    font-size: 20px;
    color: #6B7280;
}

.metric-card {
    padding: 10px;
    border-radius: 10px;
    background-color: #F8FAFC;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

try:
    df = load_data()

except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# =====================================================
# HEADER
# =====================================================

st.markdown(
    '<p class="main-header">🚀 Startup Analytics Dashboard</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-header">Executive Intelligence Platform for Startup Ecosystem Analysis</p>',
    unsafe_allow_html=True
)

st.divider()

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

summary = executive_summary(df)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Startups",
        f"{summary['total_startups']:,}"
    )

with col2:
    st.metric(
        "Funding",
        f"${summary['total_funding']:,.0f}M"
    )

with col3:
    st.metric(
        "Revenue",
        f"${summary['total_revenue']:,.0f}M"
    )

with col4:
    st.metric(
        "Valuation",
        f"${summary['total_valuation']:,.0f}M"
    )

with col5:
    st.metric(
        "Profitability",
        f"{summary['profitability_rate']}%"
    )

st.divider()

# =====================================================
# OVERVIEW
# =====================================================

left, right = st.columns([2, 1])

with left:

    st.subheader("📊 Platform Overview")

    st.write("""
This dashboard provides deep analytics into startup performance,
including:

- Funding Analytics
- Valuation Analytics
- Revenue Analytics
- Market Analytics
- Profitability Insights
- AI-Generated Recommendations
- Risk Assessment
- Startup Ranking Engine
- Growth Opportunity Analysis
""")

with right:

    st.subheader("🏆 Industry Leaders")

    st.info(
        f"Top Funding Industry: "
        f"{summary['top_funding_industry']}"
    )

    st.success(
        f"Top Revenue Industry: "
        f"{summary['top_revenue_industry']}"
    )

    st.warning(
        f"Top Valuation Industry: "
        f"{summary['top_valuation_industry']}"
    )

# =====================================================
# DATA PREVIEW
# =====================================================

st.divider()

st.subheader("📄 Dataset Preview")

st.dataframe(
    df.head(20),
    use_container_width=True
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🚀 Startup Analytics")

st.sidebar.success(
    "Use the pages menu below to navigate through analytics modules."
)

st.sidebar.markdown("""
### Available Pages

- Executive Dashboard
- Funding Analytics
- Valuation Analytics
- Revenue Analytics
- Market Analytics
- Profitability Insights
- AI Insights
""")

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "Startup Analytics Dashboard • Built with Streamlit, Pandas and Plotly"
)
