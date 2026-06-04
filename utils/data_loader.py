import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path

# ==========================================================
# REQUIRED COLUMNS
# ==========================================================

REQUIRED_COLUMNS = [
    "Startup Name",
    "Industry",
    "Funding Rounds",
    "Funding Amount (M USD)",
    "Valuation (M USD)",
    "Revenue (M USD)",
    "Employees",
    "Market Share (%)",
    "Profitable",
    "Year Founded",
    "Region",
    "Exit Status"
]

# ==========================================================
# DATA VALIDATION
# ==========================================================

def validate_columns(df):

    missing_cols = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_cols:
        raise ValueError(
            f"Missing columns: {missing_cols}"
        )

    return True


# ==========================================================
# DATA CLEANING
# ==========================================================

def clean_data(df):

    df = df.drop_duplicates()

    object_cols = df.select_dtypes(
        include=["object"]
    ).columns

    for col in object_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
        )

    numeric_cols = df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    for col in numeric_cols:
        df[col] = df[col].fillna(
            df[col].median()
        )

    categorical_cols = df.select_dtypes(
        include=["object"]
    ).columns

    for col in categorical_cols:
        df[col] = df[col].fillna(
            "Unknown"
        )

    return df


# ==========================================================
# BOOLEAN CONVERSION
# ==========================================================

def convert_profitability(df):

    if "Profitable" in df.columns:

        if df["Profitable"].dtype == object:

            df["Profitable"] = (
                df["Profitable"]
                .astype(str)
                .str.lower()
                .map({
                    "true": True,
                    "false": False,
                    "yes": True,
                    "no": False,
                    "1": True,
                    "0": False
                })
            )

    return df


# ==========================================================
# FEATURE ENGINEERING
# ==========================================================

def create_features(df):

    current_year = pd.Timestamp.now().year

    df["Startup Age"] = (
        current_year
        -
        df["Year Founded"]
    )

    df["Funding Efficiency"] = (
        df["Revenue (M USD)"]
        /
        (
            df["Funding Amount (M USD)"]
            + 1
        )
    )

    df["Valuation Multiple"] = (
        df["Valuation (M USD)"]
        /
        (
            df["Revenue (M USD)"]
            + 1
        )
    )

    df["Revenue Per Employee"] = (
        df["Revenue (M USD)"]
        /
        (
            df["Employees"]
            + 1
        )
    )

    df["Funding Per Employee"] = (
        df["Funding Amount (M USD)"]
        /
        (
            df["Employees"]
            + 1
        )
    )

    df["Growth Score"] = (
        (
            df["Revenue (M USD)"]
            *
            df["Market Share (%)"]
        )
        /
        (
            df["Funding Amount (M USD)"]
            + 1
        )
    )

    df.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    return df


# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data(show_spinner=False)
def load_data():

    try:

        file_path = (
            Path(__file__).parent.parent
            / "data"
            / "startup_data.csv"
        )

        if not file_path.exists():

            st.error(
                f"""
                ❌ Dataset not found.

                Expected location:

                {file_path}
                """
            )

            st.stop()

        df = pd.read_csv(file_path)

        validate_columns(df)

        df = clean_data(df)

        df = convert_profitability(df)

        df = create_features(df)

        return df

    except Exception as e:

        st.error(
            f"❌ Error loading dataset: {e}"
        )

        st.stop()


# ==========================================================
# FILTER DATA
# ==========================================================

def filter_data(
    df,
    industries=None,
    regions=None,
    exit_status=None
):

    filtered_df = df.copy()

    if industries:
        filtered_df = filtered_df[
            filtered_df["Industry"]
            .isin(industries)
        ]

    if regions:
        filtered_df = filtered_df[
            filtered_df["Region"]
            .isin(regions)
        ]

    if exit_status:
        filtered_df = filtered_df[
            filtered_df["Exit Status"]
            .isin(exit_status)
        ]

    return filtered_df


# ==========================================================
# SUMMARY METRICS
# ==========================================================

def get_summary_metrics(df):

    return {

        "total_startups":
            len(df),

        "total_funding":
            df["Funding Amount (M USD)"]
            .sum(),

        "total_revenue":
            df["Revenue (M USD)"]
            .sum(),

        "total_valuation":
            df["Valuation (M USD)"]
            .sum(),

        "total_employees":
            df["Employees"]
            .sum(),

        "avg_market_share":
            round(
                df["Market Share (%)"]
                .mean(),
                2
            ),

        "profitability_rate":
            round(
                df["Profitable"]
                .mean() * 100,
                2
            )
    }
