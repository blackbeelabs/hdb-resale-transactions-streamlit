import streamlit as st

st.set_page_config(layout="wide")

import pandas as pd
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

st.markdown("# Address Explorer")


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modification_container = st.container()

    with modification_container:
        user_text_input = st.text_input(
            f"Enter Address Here",
        )
        if user_text_input:
            df = df[df["Address"].str.contains(user_text_input.upper())]

    return df


df = pd.read_csv(
    os.path.join(PROJECT_DIR, "assets", "entity-transaction.csv"),
)

df = df[
    [
        "town",
        "address",
        "minimum_floor",
        "maximum_floor",
        "sqft",
        "flat_type",
        "year_of_sale",
        "month_of_sale",
        "price",
        "psf",
        "built_year",
        # "lease_band_name",
        "price_band_name",
        "psf_band_name",
    ]
]
df.columns = [
    "Town",
    "Address",
    "Min. Floor",
    "Max. Floor",
    "Area (sqft)",
    "Type",
    "Year of Sale",
    "Month of Sale",
    "Price",
    "PSF (SGD)",
    "Built Year",
    # "Lease Left (Band)",
    "Price (Band)",
    "PSF (Band)",
]

df_result = filter_dataframe(df)
max_unique_addresses = list(df["Address"].unique())
count_max_uniq_addresses = len(max_unique_addresses)
unique_addresses = list(df_result["Address"].unique())
count_uniq_addresses = len(unique_addresses)


if count_uniq_addresses == count_max_uniq_addresses:
    pass
elif count_uniq_addresses > 5:
    five_unique_addresses = (
        ", ".join(unique_addresses[:5])
        + " ... "
        + f"({count_uniq_addresses} addresses)"
    )
    st.write(f"Search results for {five_unique_addresses}")
elif count_uniq_addresses > 1:
    less_than_5unique_addresses = (
        ", ".join(unique_addresses[:-1]) + " and " + unique_addresses[-1]
    )
    st.write(f"Search results for {less_than_5unique_addresses}")
elif count_uniq_addresses == 1:
    st.write(f"Search results for {unique_addresses[0]}")
else:
    st.write(f"No search results. Please try again")

if df_result.shape[0] > 1:
    st.dataframe(
        df_result,
        hide_index=True,
        use_container_width=True,
    )
else:
    st.dataframe(
        df.head(20),
        hide_index=True,
        use_container_width=True,
    )

if df_result.shape[0] > 0:
    c = df_result.shape[0]
    st.write(f"{c:,.0f} transaction(s) found")

if count_uniq_addresses == 1:
    col1, col2, col3 = st.columns(3)
    unique_years = df[["Year of Sale"]].copy().drop_duplicates()

    count_txns = df_result.groupby("Year of Sale").size().reset_index(name="No of txns")
    count_txns = unique_years.merge(count_txns, how="left")
    count_txns = count_txns.fillna(0)

    count_room_txns = (
        df_result.groupby(["Year of Sale", "Type"])
        .size()
        .reset_index(name="No of txns")
    )
    count_room_txns = count_room_txns.merge(unique_years, how="left")
    count_room_txns = count_room_txns.fillna(0)
    count_room_txns = pd.pivot(
        count_room_txns, columns="Type", index="Year of Sale", values="No of txns"
    )
    count_room_txns = count_room_txns.fillna(0)

    col1.write(f"#### No. of Transactions by Year")
    col1.bar_chart(count_txns, x="Year of Sale", y="No of txns")
    col2.write(f"#### No. of Transactions by Type")
    col2.dataframe(
        count_room_txns,
        hide_index=True,
        use_container_width=True,
    )

    psf0 = (
        df_result.groupby("Year of Sale")["PSF (SGD)"]
        .mean()
        .reset_index(name="Mean PSF")
    )

    psf1 = (
        df_result.groupby("Year of Sale")["PSF (SGD)"]
        .mean()
        .reset_index(name="Median PSF")
    )

    psf2 = (
        df_result.groupby("Year of Sale")["PSF (SGD)"]
        .quantile(0.75)
        .reset_index(name="75th pctle PSF")
    )
    psf_df = (
        unique_years.merge(psf0, how="left")
        .merge(psf1, how="left")
        .merge(psf2, how="left")
    )
    psf_df.fillna("(No txns)", inplace=True)
    psf_df["Mean PSF"] = psf_df["Mean PSF"].apply(
        lambda x: f"${x:.2f}" if not x == "(No txns)" else x
    )
    psf_df["Median PSF"] = psf_df["Median PSF"].apply(
        lambda x: f"${x:.2f}" if not x == "(No txns)" else x
    )
    psf_df["75th pctle PSF"] = psf_df["75th pctle PSF"].apply(
        lambda x: f"${x:.2f}" if not x == "(No txns)" else x
    )
    col3.markdown("#### PSF trends")
    col3.dataframe(
        psf_df,
        hide_index=True,
        use_container_width=True,
    )
