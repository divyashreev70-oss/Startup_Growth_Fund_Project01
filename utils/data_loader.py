import streamlit as st
import pandas as pd
import numpy as np

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

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove extra spaces
    object_cols = df.select_dtypes(
        include=["object"]
    ).columns

    for col in object_cols:
        df[col] = df[col].astype(str).str.strip()

    # Fill numeric nulls
    numeric_cols = df.select_dtypes(
        include=["int64", "float64"]
    ).columns

    for col in numeric_cols:
        df[col] = df[col].fillna(
            df[col].median()
        )

    # Fill categorical nulls
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

    # Startup Age
    df["Startup Age"] = (
        current_year -
        df["Year Founded"]
    )

    # Funding Efficiency
    df["Funding Efficiency"] = (
        df["Revenue (M USD)"]
        /
        df["Funding Amount (M USD)"]
    )

    # Valuation Multiple
    df["Valuation Multiple"] = (
        df["Valuation (M USD)"]
        /
        df["Revenue (M USD)"]
    )

    # Revenue Per Employee
    df["Revenue Per Employee"] = (
        df["Revenue (M USD)"]
        /
        df["Employees"]
    )

    # Funding Per Employee
    df["Funding Per Employee"] = (
        df["Funding Amount (M USD)"]
        /
        df["Employees"]
    )

    # Growth Score
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

    # Replace infinite values
    df.replace(
        [np.inf, -np.inf],
        np.nan,
        inplace=True
    )

    return df


# ==========================================================
# MAIN LOADER
# ==========================================================

@st.cache_data(show_spinner=False)
def load_data():

    try:

        df = pd.read_csv(
            "data/startup_data.csv"
        )

        validate_columns(df)

        df = clean_data(df)

        df = convert_profitability(df)

        df = create_features(df)

        return df

    except FileNotFoundError:

        st.error(
            "❌ startup_data.csv not found in data folder."
        )

        return pd.DataFrame()

    except Exception as e:

        st.error(
            f"❌ Error loading dataset: {e}"
        )

        return pd.DataFrame()


# ==========================================================
# FILTER FUNCTION
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
            filtered_df["Industry"].isin(
                industries
            )
        ]

    if regions:
        filtered_df = filtered_df[
            filtered_df["Region"].isin(
                regions
            )
        ]

    if exit_status:
        filtered_df = filtered_df[
            filtered_df["Exit Status"].isin(
                exit_status
            )
        ]

    return filtered_df


# ==========================================================
# SUMMARY METRICS
# ==========================================================

def get_summary_metrics(df):

    metrics = {

        "total_startups":
            len(df),

        "total_funding":
            df["Funding Amount (M USD)"].sum(),

        "total_revenue":
            df["Revenue (M USD)"].sum(),

        "total_valuation":
            df["Valuation (M USD)"].sum(),

        "avg_market_share":
            df["Market Share (%)"].mean(),

        "profitability_rate":
            (
                df["Profitable"].mean()
                * 100
            )
    }

    return metrics
