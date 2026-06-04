import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------

st.set_page_config(
    page_title="Funding Analytics",
    page_icon="💸",
    layout="wide"
)

# -----------------------------------------------------
# LOAD DATA
# -----------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/startup_data.csv")

df = load_data()

# -----------------------------------------------------
# PAGE HEADER
# -----------------------------------------------------

st.title("💸 Funding Analytics Dashboard")

st.markdown("""
Analyze startup funding patterns, investment concentration,
industry funding distribution, regional trends, and capital efficiency.
""")

# -----------------------------------------------------
# SIDEBAR FILTERS
# -----------------------------------------------------

st.sidebar.header("Filters")

industry = st.sidebar.multiselect(
    "Industry",
    sorted(df["Industry"].unique()),
    default=sorted(df["Industry"].unique())
)

region = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

funding_range = st.sidebar.slider(
    "Funding Amount (M USD)",
    int(df["Funding Amount (M USD)"].min()),
    int(df["Funding Amount (M USD)"].max()),
    (
        int(df["Funding Amount (M USD)"].min()),
        int(df["Funding Amount (M USD)"].max())
    )
)

filtered_df = df[
    (df["Industry"].isin(industry))
    &
    (df["Region"].isin(region))
    &
    (
        df["Funding Amount (M USD)"].between(
            funding_range[0],
            funding_range[1]
        )
    )
]

# -----------------------------------------------------
# KPI SECTION
# -----------------------------------------------------

st.subheader("📊 Funding KPIs")

total_funding = filtered_df["Funding Amount (M USD)"].sum()

avg_funding = filtered_df["Funding Amount (M USD)"].mean()

median_funding = filtered_df["Funding Amount (M USD)"].median()

max_funding = filtered_df["Funding Amount (M USD)"].max()

total_rounds = filtered_df["Funding Rounds"].sum()

avg_rounds = filtered_df["Funding Rounds"].mean()

c1,c2,c3,c4,c5,c6 = st.columns(6)

c1.metric(
    "Total Funding",
    f"${total_funding:,.0f}M"
)

c2.metric(
    "Average Funding",
    f"${avg_funding:,.1f}M"
)

c3.metric(
    "Median Funding",
    f"${median_funding:,.1f}M"
)

c4.metric(
    "Largest Round",
    f"${max_funding:,.0f}M"
)

c5.metric(
    "Funding Rounds",
    f"{total_rounds:,.0f}"
)

c6.metric(
    "Avg Rounds",
    f"{avg_rounds:.1f}"
)

st.divider()

# -----------------------------------------------------
# INDUSTRY FUNDING
# -----------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    industry_funding = (
        filtered_df
        .groupby("Industry")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
        .sort_values(
            "Funding Amount (M USD)",
            ascending=False
        )
    )

    fig = px.bar(
        industry_funding,
        x="Industry",
        y="Funding Amount (M USD)",
        title="Funding by Industry",
        text_auto=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.pie(
        industry_funding,
        names="Industry",
        values="Funding Amount (M USD)",
        title="Industry Funding Share"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------------------------------------
# REGION ANALYSIS
# -----------------------------------------------------

st.subheader("🌍 Regional Funding Analysis")

region_funding = (
    filtered_df
    .groupby("Region")
    ["Funding Amount (M USD)"]
    .sum()
    .reset_index()
)

fig = px.treemap(
    region_funding,
    path=["Region"],
    values="Funding Amount (M USD)",
    title="Regional Funding Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------------------------
# FUNDING DISTRIBUTION
# -----------------------------------------------------

col1,col2 = st.columns(2)

with col1:

    fig = px.histogram(
        filtered_df,
        x="Funding Amount (M USD)",
        nbins=30,
        title="Funding Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.box(
        filtered_df,
        y="Funding Amount (M USD)",
        x="Industry",
        title="Funding Spread by Industry"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------------------------------------
# FUNDING VS VALUATION
# -----------------------------------------------------

st.subheader("💰 Funding vs Valuation")

fig = px.scatter(
    filtered_df,
    x="Funding Amount (M USD)",
    y="Valuation (M USD)",
    size="Revenue (M USD)",
    color="Industry",
    hover_name="Startup Name",
    title="Capital Raised vs Valuation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------------------------
# FUNDING ROUNDS ANALYSIS
# -----------------------------------------------------

st.subheader("🔄 Funding Rounds Analysis")

rounds_df = (
    filtered_df
    .groupby("Funding Rounds")
    .size()
    .reset_index(name="Count")
)

fig = px.bar(
    rounds_df,
    x="Funding Rounds",
    y="Count",
    title="Distribution of Funding Rounds"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------------------------
# FUNDING EFFICIENCY
# -----------------------------------------------------

st.subheader("⚡ Funding Efficiency")

efficiency_df = filtered_df.copy()

efficiency_df["Valuation_to_Funding"] = (
    efficiency_df["Valuation (M USD)"]
    /
    efficiency_df["Funding Amount (M USD)"]
)

top_efficiency = (
    efficiency_df
    .sort_values(
        "Valuation_to_Funding",
        ascending=False
    )
    .head(15)
)

fig = px.bar(
    top_efficiency,
    x="Startup Name",
    y="Valuation_to_Funding",
    title="Top Capital Efficient Startups"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------------------------
# TOP FUNDED STARTUPS
# -----------------------------------------------------

st.subheader("🏆 Top Funded Startups")

top_funded = (
    filtered_df
    .sort_values(
        "Funding Amount (M USD)",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_funded[
        [
            "Startup Name",
            "Industry",
            "Funding Amount (M USD)",
            "Valuation (M USD)",
            "Revenue (M USD)",
            "Region"
        ]
    ],
    use_container_width=True
)

# -----------------------------------------------------
# CORRELATION ANALYSIS
# -----------------------------------------------------

st.subheader("🔥 Funding Correlation Analysis")

numeric_cols = [
    "Funding Amount (M USD)",
    "Funding Rounds",
    "Valuation (M USD)",
    "Revenue (M USD)",
    "Employees",
    "Market Share (%)"
]

corr = filtered_df[numeric_cols].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    title="Funding Relationship Matrix"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------------------------
# AUTOMATED INSIGHTS
# -----------------------------------------------------

st.subheader("🤖 Funding Insights")

top_industry = (
    filtered_df.groupby("Industry")
    ["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

top_region = (
    filtered_df.groupby("Region")
    ["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

most_funded = (
    filtered_df.sort_values(
        "Funding Amount (M USD)",
        ascending=False
    )
    .iloc[0]
)

st.success(
    f"Highest funded industry: {top_industry}"
)

st.success(
    f"Most active funding region: {top_region}"
)

st.success(
    f"Largest funded startup: "
    f"{most_funded['Startup Name']} "
    f"(${most_funded['Funding Amount (M USD)']:,.0f}M)"
)

# -----------------------------------------------------
# DOWNLOAD DATA
# -----------------------------------------------------

st.subheader("⬇ Download Filtered Data")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="funding_analytics.csv",
    mime="text/csv"
)

# -----------------------------------------------------
# FOOTER
# -----------------------------------------------------

st.divider()

st.caption(
    "Funding Analytics Module | Startup Intelligence Platform"
)
