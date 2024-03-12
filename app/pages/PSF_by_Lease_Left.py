import streamlit as st

st.set_page_config(layout="wide")

import pandas as pd
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
df = pd.read_csv(
    os.path.join(PROJECT_DIR, "assets", "entity-transaction.csv"),
)

st.markdown("# Price Trend (PSF) by Lease Left")

col1, col2 = st.columns(2)
counter = 0
years_of_sale = df["year_of_sale"].copy().drop_duplicates()
years_of_sale = years_of_sale.sort_values(ascending=False)
for yr in years_of_sale:
    dfyr = df[df["year_of_sale"] == yr].copy()
    dfyr["lease_left"] = 99 - (yr - dfyr["built_year"])
    dfyr = dfyr[
        [
            "year_of_sale",
            "built_year",
            "lease_left",
            "price",
            "psf",
        ]
    ]
    dfyr_mean = dfyr.groupby("lease_left")["psf"].mean().reset_index(name="Mean PSF")
    dfyr_median = (
        dfyr.groupby("lease_left")["psf"].median().reset_index(name="Median PSF")
    )
    dfyr_pct95 = (
        dfyr.groupby("lease_left")["psf"]
        .quantile(0.95)
        .reset_index(name="95th Pctile PSF")
    )
    dfyr_pct25 = (
        dfyr.groupby("lease_left")["psf"]
        .quantile(0.25)
        .reset_index(name="25th Pctile PSF")
    )
    dfyr_agg = dfyr_mean.merge(dfyr_median).merge(dfyr_pct95).merge(dfyr_pct25)
    if counter % 2 == 0:
        col1.markdown(f"#### {yr}")
        col1.line_chart(dfyr_agg, x="lease_left")
    elif counter % 2 == 1:
        col2.markdown(f"#### {yr}")
        col2.line_chart(dfyr_agg, x="lease_left")
    counter += 1
