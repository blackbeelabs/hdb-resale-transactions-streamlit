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


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("ADD FILTERS")

    if not modify:
        return df

    df = df.copy()

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter transactions on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write(">")
            if df[column].nunique() < 30:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    _min,
                    _max,
                    (_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input.upper())]

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


st.markdown("# Transactions Explorer")
st.markdown(
    "To explore, simply check the _ADD FILTERS_ checkbox and select the columns to filter on."
)
df_result = filter_dataframe(df)

if df_result.shape[0] > 1:
    st.dataframe(df_result)
else:
    st.markdown(f"No search results. Please try again")
    st.markdown(f"(Displaying a sample)")
    st.dataframe(df.head(4))
if df_result.shape[0] > 0:
    c = df_result.shape[0]
    st.markdown(f"{c:,.0f} transaction(s) found")
