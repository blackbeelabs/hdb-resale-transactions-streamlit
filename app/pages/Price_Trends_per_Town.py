import streamlit as st

st.set_page_config(layout="wide")

import pandas as pd
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

st.markdown("# Price Trend Charts by Town")


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    modification_container = st.container()

    with modification_container:
        s1, _, _ = st.columns(3)
        user_cat_input = s1.selectbox(
            f"Select town",
            df["town"].unique(),
        )
        df = df[df["town"] == (user_cat_input)]

    return df


df = pd.read_csv(
    os.path.join(PROJECT_DIR, "assets", "entity-transaction.csv"),
)
dftown = filter_dataframe(df)
town = dftown["town"].unique()[0]


dftown = df[df["town"] == town]
dftown_mean = (
    dftown.groupby("year_of_sale")["price"].mean().reset_index(name="Mean Price")
)
dftown_median = (
    dftown.groupby("year_of_sale")["price"].median().reset_index(name="Median Price")
)
dftown_p75 = (
    dftown.groupby("year_of_sale")["price"]
    .quantile(0.75)
    .reset_index(name="75 Pctle Price")
)
dftown_p90 = (
    dftown.groupby("year_of_sale")["price"]
    .quantile(0.90)
    .reset_index(name="90 Pctle Price")
)
dftown_max = dftown.groupby("year_of_sale")["price"].max().reset_index(name="Max Price")
dftown_agg = (
    dftown_mean.merge(dftown_max)
    .merge(dftown_median)
    .merge(dftown_p75)
    .merge(dftown_p90)
)

psf_mean = dftown.groupby("year_of_sale")["psf"].mean().reset_index(name="Mean PSF")
psf_median = (
    dftown.groupby("year_of_sale")["psf"].median().reset_index(name="Median PSF")
)
psf_p75 = (
    dftown.groupby("year_of_sale")["psf"]
    .quantile(0.75)
    .reset_index(name="75 Pctle PSF")
)
psf_p90 = (
    dftown.groupby("year_of_sale")["psf"]
    .quantile(0.90)
    .reset_index(name="90 Pctle PSF")
)
psf_max = dftown.groupby("year_of_sale")["psf"].max().reset_index(name="Max PSF")
psf_agg = psf_mean.merge(psf_max).merge(psf_median).merge(psf_p75).merge(psf_p90)
col1, col2 = st.columns(2)
col1.markdown(f"#### Price Trend for {town}")
col1.line_chart(dftown_agg, x="year_of_sale")
col2.markdown(f"#### PSF Trend for {town}")
col2.line_chart(psf_agg, x="year_of_sale")
