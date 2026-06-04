import pandas as pd
import numpy as np

# =====================================================
# BASIC KPIs
# =====================================================

def get_total_startups(df):
    return len(df)


def get_total_funding(df):
    return df["Funding Amount (M USD)"].sum()


def get_total_revenue(df):
    return df["Revenue (M USD)"].sum()


def get_total_valuation(df):
    return df["Valuation (M USD)"].sum()


def get_total_employees(df):
    return df["Employees"].sum()


def get_profitability_rate(df):
    return round(
        df["Profitable"].mean() * 100,
        2
    )


# =====================================================
# TOP INDUSTRY
# =====================================================

def top_industry(df, metric):

    return (
        df.groupby("Industry")[metric]
        .sum()
        .idxmax()
    )


# =====================================================
# TOP REGION
# =====================================================

def top_region(df, metric):

    return (
        df.groupby("Region")[metric]
        .sum()
        .idxmax()
    )


# =====================================================
# TOP STARTUP
# =====================================================

def top_startup(df, metric):

    row = (
        df.sort_values(
            metric,
            ascending=False
        )
        .iloc[0]
    )

    return {
        "name": row["Startup Name"],
        "value": row[metric]
    }


# =====================================================
# FUNDING EFFICIENCY
# =====================================================

def calculate_funding_efficiency(df):

    temp = df.copy()

    temp["Funding Efficiency"] = (
        temp["Revenue (M USD)"]
        /
        temp["Funding Amount (M USD)"]
    )

    temp.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    return temp


# =====================================================
# VALUATION MULTIPLE
# =====================================================

def calculate_valuation_multiple(df):

    temp = df.copy()

    temp["Valuation Multiple"] = (
        temp["Valuation (M USD)"]
        /
        temp["Revenue (M USD)"]
    )

    temp.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    return temp


# =====================================================
# REVENUE EFFICIENCY
# =====================================================

def calculate_revenue_per_employee(df):

    temp = df.copy()

    temp["Revenue Per Employee"] = (
        temp["Revenue (M USD)"]
        /
        temp["Employees"]
    )

    temp.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    return temp


# =====================================================
# STARTUP SCORING ENGINE
# =====================================================

def startup_scoring(df):

    score_df = df.copy()

    score_df["Funding Efficiency"] = (
        score_df["Revenue (M USD)"]
        /
        score_df["Funding Amount (M USD)"]
    )

    score_df.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    score_df.fillna(0, inplace=True)

    score_df["Startup Score"] = (

        score_df["Revenue (M USD)"] * 0.35

        +

        score_df["Market Share (%)"] * 0.25

        +

        score_df["Valuation (M USD)"] * 0.25

        +

        score_df["Funding Efficiency"] * 100 * 0.15
    )

    return (
        score_df
        .sort_values(
            "Startup Score",
            ascending=False
        )
    )


# =====================================================
# GROWTH SCORE
# =====================================================

def calculate_growth_score(df):

    growth_df = df.copy()

    growth_df["Growth Score"] = (

        growth_df["Revenue (M USD)"]

        *

        growth_df["Market Share (%)"]

    ) / (

        growth_df["Funding Amount (M USD)"]

        + 1

    )

    return growth_df


# =====================================================
# RISK ANALYSIS
# =====================================================

def calculate_risk_score(df):

    risk_df = df.copy()

    risk_df["Risk Score"] = (

        risk_df["Funding Amount (M USD)"]

        /

        (

            risk_df["Revenue (M USD)"]

            + 1

        )

    )

    return (
        risk_df
        .sort_values(
            "Risk Score",
            ascending=False
        )
    )


# =====================================================
# UNICORN DETECTION
# =====================================================

def get_unicorns(df):

    return df[
        df["Valuation (M USD)"] >= 1000
    ]


# =====================================================
# OUTLIER DETECTION
# =====================================================

def detect_valuation_outliers(df):

    q1 = df[
        "Valuation (M USD)"
    ].quantile(0.25)

    q3 = df[
        "Valuation (M USD)"
    ].quantile(0.75)

    iqr = q3 - q1

    outliers = df[
        (
            df["Valuation (M USD)"]
            >
            q3 + 1.5 * iqr
        )
    ]

    return outliers


# =====================================================
# INDUSTRY SUMMARY
# =====================================================

def industry_summary(df):

    return (
        df.groupby("Industry")
        .agg({
            "Funding Amount (M USD)": "sum",
            "Revenue (M USD)": "sum",
            "Valuation (M USD)": "sum",
            "Employees": "sum",
            "Market Share (%)": "mean"
        })
        .reset_index()
    )


# =====================================================
# REGION SUMMARY
# =====================================================

def region_summary(df):

    return (
        df.groupby("Region")
        .agg({
            "Funding Amount (M USD)": "sum",
            "Revenue (M USD)": "sum",
            "Valuation (M USD)": "sum",
            "Employees": "sum",
            "Market Share (%)": "mean"
        })
        .reset_index()
    )


# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

def executive_summary(df):

    return {
        "total_startups":
            get_total_startups(df),

        "total_funding":
            get_total_funding(df),

        "total_revenue":
            get_total_revenue(df),

        "total_valuation":
            get_total_valuation(df),

        "profitability_rate":
            get_profitability_rate(df),

        "top_funding_industry":
            top_industry(
                df,
                "Funding Amount (M USD)"
            ),

        "top_revenue_industry":
            top_industry(
                df,
                "Revenue (M USD)"
            ),

        "top_valuation_industry":
            top_industry(
                df,
                "Valuation (M USD)"
            )
    }


# =====================================================
# AI INSIGHTS GENERATOR
# =====================================================

def generate_ai_insights(df):

    insights = []

    try:

        funding_leader = top_industry(
            df,
            "Funding Amount (M USD)"
        )

        revenue_leader = top_industry(
            df,
            "Revenue (M USD)"
        )

        valuation_leader = top_industry(
            df,
            "Valuation (M USD)"
        )

        profitability = (
            get_profitability_rate(df)
        )

        insights.append(
            f"Highest funded industry is {funding_leader}."
        )

        insights.append(
            f"Highest revenue-generating industry is {revenue_leader}."
        )

        insights.append(
            f"Highest valuation industry is {valuation_leader}."
        )

        insights.append(
            f"Overall profitability rate is {profitability:.2f}%."
        )

        if profitability >= 50:
            insights.append(
                "More than half of startups are profitable."
            )
        else:
            insights.append(
                "Less than half of startups are profitable."
            )

    except Exception as e:

        insights.append(
            f"Insight generation error: {str(e)}"
        )

    return insights


# =====================================================
# RECOMMENDATIONS
# =====================================================

def generate_recommendations(df):

    recommendations = []

    funding_industry = top_industry(
        df,
        "Funding Amount (M USD)"
    )

    revenue_industry = top_industry(
        df,
        "Revenue (M USD)"
    )

    recommendations.append(
        f"Consider increasing investments in {revenue_industry}."
    )

    recommendations.append(
        f"Monitor capital deployment in {funding_industry}."
    )

    recommendations.append(
        "Focus on startups with strong funding efficiency."
    )

    recommendations.append(
        "Prioritize companies with growing market share."
    )

    recommendations.append(
        "Review high-risk startups before additional funding."
    )

    return recommendations
