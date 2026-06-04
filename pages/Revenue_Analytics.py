import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Revenue Analytics",
    page_icon="📈",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    return pd.read_csv("data/startup_data.csv")

df = load_data()

# ==========================================================
# HEADER
# ==========================================================

st.title("📈 Revenue Analytics Dashboard")

st.markdown("""
Analyze revenue performance, operational efficiency,
industry benchmarks, and startup growth indicators.
""")

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.header("Revenue Filters")

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

revenue_range = st.sidebar.slider(
    "Revenue (M USD)",
    int(df["Revenue (M USD)"].min()),
    int(df["Revenue (M USD)"].max()),
    (
        int(df["Revenue (M USD)"].min()),
        int(df["Revenue (M USD)"].max())
    )
)

filtered_df = df[
    (df["Industry"].isin(industry))
    &
    (df["Region"].isin(region))
    &
    (
        filtered_df["Revenue (M USD)"].between(
            revenue_range[0],
            revenue_range[1]
        )
    )
] if False else df[
    (df["Industry"].isin(industry))
    &
    (df["Region"].isin(region))
    &
    (
        df["Revenue (M USD)"].between(
            revenue_range[0],
            revenue_range[1]
        )
    )
]

# ==========================================================
# KPI SECTION
# ==========================================================

st.subheader("📊 Revenue KPIs")

total_revenue = filtered_df["Revenue (M USD)"].sum()

avg_revenue = filtered_df["Revenue (M USD)"].mean()

median_revenue = filtered_df["Revenue (M USD)"].median()

max_revenue = filtered_df["Revenue (M USD)"].max()

total_employees = filtered_df["Employees"].sum()

revenue_per_employee = (
    total_revenue / total_employees
    if total_employees > 0
    else 0
)

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric(
    "Total Revenue",
    f"${total_revenue:,.0f}M"
)

c2.metric(
    "Average Revenue",
    f"${avg_revenue:,.1f}M"
)

c3.metric(
    "Median Revenue",
    f"${median_revenue:,.1f}M"
)

c4.metric(
    "Highest Revenue",
    f"${max_revenue:,.0f}M"
)

c5.metric(
    "Employees",
    f"{total_employees:,}"
)

c6.metric(
    "Revenue/Employee",
    f"${revenue_per_employee:.2f}M"
)

st.divider()

# ==========================================================
# REVENUE DISTRIBUTION
# ==========================================================

col1, col2 = st.columns(2)

with col1:

    fig = px.histogram(
        filtered_df,
        x="Revenue (M USD)",
        nbins=30,
        title="Revenue Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.box(
        filtered_df,
        x="Industry",
        y="Revenue (M USD)",
        title="Revenue Spread by Industry"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# INDUSTRY REVENUE ANALYSIS
# ==========================================================

st.subheader("🏭 Revenue by Industry")

industry_revenue = (
    filtered_df
    .groupby("Industry")
    ["Revenue (M USD)"]
    .sum()
    .reset_index()
    .sort_values(
        "Revenue (M USD)",
        ascending=False
    )
)

fig = px.bar(
    industry_revenue,
    x="Industry",
    y="Revenue (M USD)",
    text_auto=True,
    title="Industry Revenue Ranking"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# REGION ANALYSIS
# ==========================================================

st.subheader("🌍 Revenue by Region")

region_revenue = (
    filtered_df
    .groupby("Region")
    ["Revenue (M USD)"]
    .sum()
    .reset_index()
)

fig = px.treemap(
    region_revenue,
    path=["Region"],
    values="Revenue (M USD)",
    title="Regional Revenue Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# REVENUE VS EMPLOYEES
# ==========================================================

st.subheader("👥 Revenue vs Employees")

fig = px.scatter(
    filtered_df,
    x="Employees",
    y="Revenue (M USD)",
    size="Valuation (M USD)",
    color="Industry",
    hover_name="Startup Name",
    title="Employee Productivity Analysis"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# REVENUE VS FUNDING
# ==========================================================

st.subheader("💸 Revenue vs Funding")

fig = px.scatter(
    filtered_df,
    x="Funding Amount (M USD)",
    y="Revenue (M USD)",
    size="Valuation (M USD)",
    color="Region",
    hover_name="Startup Name",
    title="Funding Efficiency"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# REVENUE PER EMPLOYEE
# ==========================================================

st.subheader("⚡ Revenue Efficiency")

eff_df = filtered_df.copy()

eff_df["Revenue Per Employee"] = (
    eff_df["Revenue (M USD)"]
    /
    eff_df["Employees"]
)

eff_df = eff_df.replace(
    [np.inf, -np.inf],
    np.nan
).dropna()

top_eff = (
    eff_df
    .sort_values(
        "Revenue Per Employee",
        ascending=False
    )
    .head(20)
)

fig = px.bar(
    top_eff,
    x="Startup Name",
    y="Revenue Per Employee",
    title="Top Revenue Efficient Startups"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# MARKET SHARE VS REVENUE
# ==========================================================

st.subheader("📊 Revenue vs Market Share")

fig = px.scatter(
    filtered_df,
    x="Market Share (%)",
    y="Revenue (M USD)",
    color="Industry",
    size="Employees",
    hover_name="Startup Name",
    title="Market Share Impact on Revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# TOP REVENUE STARTUPS
# ==========================================================

st.subheader("🏆 Top Revenue Startups")

top_revenue = (
    filtered_df
    .sort_values(
        "Revenue (M USD)",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_revenue[
        [
            "Startup Name",
            "Industry",
            "Revenue (M USD)",
            "Valuation (M USD)",
            "Funding Amount (M USD)",
            "Employees",
            "Region"
        ]
    ],
    use_container_width=True
)

# ==========================================================
# CORRELATION HEATMAP
# ==========================================================

st.subheader("🔥 Revenue Correlation Analysis")

numeric_cols = [
    "Revenue (M USD)",
    "Funding Amount (M USD)",
    "Valuation (M USD)",
    "Employees",
    "Market Share (%)",
    "Funding Rounds"
]

corr = filtered_df[numeric_cols].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    title="Revenue Correlation Matrix"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# AUTOMATED INSIGHTS
# ==========================================================

st.subheader("🤖 Revenue Insights")

top_industry = (
    filtered_df.groupby("Industry")
    ["Revenue (M USD)"]
    .sum()
    .idxmax()
)

top_region = (
    filtered_df.groupby("Region")
    ["Revenue (M USD)"]
    .sum()
    .idxmax()
)

best_company = (
    filtered_df
    .sort_values(
        "Revenue (M USD)",
        ascending=False
    )
    .iloc[0]
)

st.success(
    f"Highest revenue industry: {top_industry}"
)

st.success(
    f"Top revenue region: {top_region}"
)

st.success(
    f"Highest revenue startup: "
    f"{best_company['Startup Name']} "
    f"(${best_company['Revenue (M USD)']:,.0f}M)"
)

st.success(
    f"Average revenue per employee across filtered startups: "
    f"${revenue_per_employee:.2f}M"
)

# ==========================================================
# DOWNLOAD DATA
# ==========================================================

st.subheader("⬇ Download Revenue Data")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Revenue Analytics CSV",
    data=csv,
    file_name="revenue_analytics.csv",
    mime="text/csv"
)

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "Revenue Analytics Module | Startup Intelligence Platform"
)
