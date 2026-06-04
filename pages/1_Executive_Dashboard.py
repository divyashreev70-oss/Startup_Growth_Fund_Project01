import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/startup_data.csv")

df = load_data()

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color:#f8fafc;
}

.metric-card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 2px 8px rgba(0,0,0,0.08);
}

h1,h2,h3{
    color:#0f172a;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# HEADER
# ---------------------------------------------------

st.title("🚀 Startup Executive Dashboard")

st.markdown("""
Comprehensive analytics platform for startup ecosystem intelligence,
funding analysis, valuation trends, profitability insights and market analytics.
""")

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.header("🔍 Filters")

industry = st.sidebar.multiselect(
    "Industry",
    options=sorted(df["Industry"].unique()),
    default=sorted(df["Industry"].unique())
)

region = st.sidebar.multiselect(
    "Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

exit_status = st.sidebar.multiselect(
    "Exit Status",
    options=sorted(df["Exit Status"].unique()),
    default=sorted(df["Exit Status"].unique())
)

year_range = st.sidebar.slider(
    "Year Founded",
    int(df["Year Founded"].min()),
    int(df["Year Founded"].max()),
    (
        int(df["Year Founded"].min()),
        int(df["Year Founded"].max())
    )
)

# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------

filtered_df = df[
    (df["Industry"].isin(industry))
    &
    (df["Region"].isin(region))
    &
    (df["Exit Status"].isin(exit_status))
    &
    (df["Year Founded"].between(
        year_range[0],
        year_range[1]
    ))
]

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

st.subheader("📊 Key Performance Indicators")

total_startups = len(filtered_df)

total_funding = filtered_df["Funding Amount (M USD)"].sum()

avg_valuation = filtered_df["Valuation (M USD)"].mean()

total_revenue = filtered_df["Revenue (M USD)"].sum()

total_employees = filtered_df["Employees"].sum()

profitability_rate = (
    filtered_df["Profitable"].mean()*100
)

c1,c2,c3,c4,c5,c6 = st.columns(6)

c1.metric(
    "Startups",
    f"{total_startups:,}"
)

c2.metric(
    "Funding",
    f"${total_funding:,.0f}M"
)

c3.metric(
    "Avg Valuation",
    f"${avg_valuation:,.0f}M"
)

c4.metric(
    "Revenue",
    f"${total_revenue:,.0f}M"
)

c5.metric(
    "Employees",
    f"{total_employees:,}"
)

c6.metric(
    "Profitability",
    f"{profitability_rate:.1f}%"
)

st.divider()

# ---------------------------------------------------
# FUNDING ANALYTICS
# ---------------------------------------------------

col1,col2 = st.columns(2)

with col1:

    funding_industry = (
        filtered_df.groupby("Industry")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
        .sort_values(
            "Funding Amount (M USD)",
            ascending=False
        )
    )

    fig = px.bar(
        funding_industry,
        x="Industry",
        y="Funding Amount (M USD)",
        title="Funding by Industry"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    funding_region = (
        filtered_df.groupby("Region")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        funding_region,
        names="Region",
        values="Funding Amount (M USD)",
        title="Funding Distribution by Region"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------------------------------
# VALUATION ANALYSIS
# ---------------------------------------------------

st.subheader("💰 Valuation Intelligence")

fig = px.scatter(
    filtered_df,
    x="Funding Amount (M USD)",
    y="Valuation (M USD)",
    color="Industry",
    size="Revenue (M USD)",
    hover_name="Startup Name",
    title="Funding vs Valuation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# REVENUE ANALYSIS
# ---------------------------------------------------

col1,col2 = st.columns(2)

with col1:

    revenue_industry = (
        filtered_df.groupby("Industry")
        ["Revenue (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        revenue_industry,
        x="Industry",
        y="Revenue (M USD)",
        title="Revenue by Industry"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.scatter(
        filtered_df,
        x="Employees",
        y="Revenue (M USD)",
        color="Industry",
        title="Employees vs Revenue"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ---------------------------------------------------
# MARKET SHARE ANALYSIS
# ---------------------------------------------------

st.subheader("🌎 Market Share Analytics")

market_share = (
    filtered_df.groupby("Industry")
    ["Market Share (%)"]
    .mean()
    .reset_index()
)

fig = px.treemap(
    market_share,
    path=["Industry"],
    values="Market Share (%)",
    title="Industry Market Share"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# PROFITABILITY ANALYSIS
# ---------------------------------------------------

st.subheader("📈 Profitability Analysis")

profitability = (
    filtered_df.groupby("Profitable")
    .size()
    .reset_index(name="Count")
)

fig = px.pie(
    profitability,
    names="Profitable",
    values="Count",
    title="Profitable vs Non-Profitable"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# CORRELATION HEATMAP
# ---------------------------------------------------

st.subheader("🔥 Correlation Analysis")

numeric_df = filtered_df.select_dtypes(
    include=["int64","float64"]
)

corr = numeric_df.corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Correlation Heatmap"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# TOP STARTUPS
# ---------------------------------------------------

st.subheader("🏆 Top 20 Startups by Valuation")

top20 = (
    filtered_df
    .sort_values(
        "Valuation (M USD)",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top20[
        [
            "Startup Name",
            "Industry",
            "Valuation (M USD)",
            "Revenue (M USD)",
            "Funding Amount (M USD)",
            "Region"
        ]
    ],
    use_container_width=True
)

# ---------------------------------------------------
# AI GENERATED INSIGHTS
# ---------------------------------------------------

st.subheader("🤖 AI Business Insights")

highest_funding_industry = (
    filtered_df.groupby("Industry")
    ["Funding Amount (M USD)"]
    .mean()
    .idxmax()
)

highest_valuation_industry = (
    filtered_df.groupby("Industry")
    ["Valuation (M USD)"]
    .mean()
    .idxmax()
)

top_region = (
    filtered_df.groupby("Region")
    ["Valuation (M USD)"]
    .sum()
    .idxmax()
)

st.success(
    f"Highest average funding industry: "
    f"**{highest_funding_industry}**"
)

st.success(
    f"Highest average valuation industry: "
    f"**{highest_valuation_industry}**"
)

st.success(
    f"Top performing region by valuation: "
    f"**{top_region}**"
)

st.success(
    f"Profitability Rate: "
    f"**{profitability_rate:.2f}%**"
)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.divider()

st.caption(
    "Startup Intelligence Dashboard | Streamlit + Plotly + Python"
)
