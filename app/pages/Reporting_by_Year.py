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

st.markdown("##### Report by Year")


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    modification_container = st.container()

    with modification_container:
        s1, _, _ = st.columns(3)
        s = df["Year of Sale"].sort_values(ascending=False).copy().unique()
        user_cat_input = s1.selectbox(
            f"Select year",
            s,
            index=0,
        )
        df = df[df["Year of Sale"] == (user_cat_input)]
        return user_cat_input, df


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

y, df_result = filter_dataframe(df)


st.markdown(f"# Transactions Summary for {y}")
st.markdown(f"There were {df_result.shape[0]:,.0f} transactions in {y}.")

volume = df_result.groupby("Type").size().reset_index(name="No of txns")
avg_psf = df_result.groupby("Type")["PSF (SGD)"].mean().reset_index(name="Mean PSF")
avg_psf = df_result.groupby("Type")["PSF (SGD)"].mean().reset_index(name="Mean PSF")
avg_psf["Mean PSF"] = avg_psf["Mean PSF"].apply(lambda x: f"${x:,.2f}")

c1 = volume.copy()
st.markdown("##### Volume by Type")
l1, l2 = st.columns(2)
l1.dataframe(
    c1,
    hide_index=True,
    use_container_width=True,
)
l2.bar_chart(c1, x="Type")

vol_by_town = df_result.groupby("Town").size().reset_index(name="No of txns")
st.markdown("##### Volume by Towns")
st.bar_chart(vol_by_town, x="Town")

st.markdown("Further broken down by type")
vol_by_town_by_type = (
    df_result.groupby(["Town", "Type"]).size().reset_index(name="No of txns")
)
vol_by_town_by_type_p = pd.pivot(
    vol_by_town_by_type, index="Town", columns="Type", values="No of txns"
)
st.dataframe(vol_by_town_by_type_p.fillna(0).transpose())

lease_left = df_result.copy()
lease_left["Lease Left"] = 99 - (y - lease_left["Built Year"])
by_lease_left = lease_left.groupby("Lease Left").size().reset_index(name="No of txns")
st.markdown("##### Volume by Lease Left")
st.bar_chart(by_lease_left, x="Lease Left")

psf_by_lease_left = (
    lease_left.groupby("Lease Left")["PSF (SGD)"]
    .median()
    .reset_index(name="Median PSF")
)
st.markdown("##### PSF (Median) by Lease Left")
st.bar_chart(psf_by_lease_left, x="Lease Left")


price = (
    df_result.groupby(["Town", "Type"])["Price"].mean().reset_index(name="Mean Price")
)
price_p = pd.pivot(price, index="Type", columns="Town", values="Mean Price")
for c in price_p.columns:
    price_p[c] = price_p[c].fillna("(No txns)")
    price_p[c] = price_p[c].apply(
        lambda x: "(No txns)" if x == "(No txns)" else f"${x:,.0f}"
    )
st.markdown("##### Mean Price by Town, Type")

st.dataframe(price_p)

pricem = (
    df_result.groupby(["Town", "Type"])["Price"]
    .median()
    .reset_index(name="Median Price")
)
pricem_p = pd.pivot(pricem, index="Type", columns="Town", values="Median Price")
for c in pricem_p.columns:
    pricem_p[c] = pricem_p[c].fillna("(No txns)")
    pricem_p[c] = pricem_p[c].apply(
        lambda x: "(No txns)" if x == "(No txns)" else f"${x:,.0f}"
    )
st.markdown("##### Median Price by Town, Type")
st.dataframe(pricem_p)
