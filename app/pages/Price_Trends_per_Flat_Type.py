import streamlit as st

st.set_page_config(layout="wide")

import pandas as pd
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
df = pd.read_csv(
    os.path.join(PROJECT_DIR, "assets", "entity-transaction.csv"),
)
flat_types = df["flat_type"].unique()

st.markdown("# Price Trend Charts per Flat Type")

counter = 0
for type in flat_types:

    dftown = df[df["flat_type"] == type]
    dftown_txns = df.groupby("year_of_sale").size().reset_index(name="Number of Txns")

    dftown_mean = (
        dftown.groupby("year_of_sale")["price"].mean().reset_index(name="Mean Price")
    )
    dftown_median = (
        dftown.groupby("year_of_sale")["price"]
        .median()
        .reset_index(name="Median Price")
    )
    dftown_p90 = (
        dftown.groupby("year_of_sale")["price"]
        .quantile(0.90)
        .reset_index(name="90th pctle of Price")
    )
    dftown_max = (
        dftown.groupby("year_of_sale")["price"].max().reset_index(name="Max Price")
    )
    dftown_agg = dftown_mean.merge(dftown_max).merge(dftown_median).merge(dftown_p90)

    dfpsf_mean = (
        dftown.groupby("year_of_sale")["psf"].mean().reset_index(name="Mean PSF")
    )
    dfpsf_median = (
        dftown.groupby("year_of_sale")["psf"].median().reset_index(name="Median PSF")
    )
    dfpsf_p90 = (
        dftown.groupby("year_of_sale")["psf"]
        .quantile(0.90)
        .reset_index(name="90th pctle of PSF")
    )
    dfpsf_max = dftown.groupby("year_of_sale")["psf"].max().reset_index(name="Max PSF")
    dfpsf_agg = dfpsf_mean.merge(dfpsf_max).merge(dfpsf_median).merge(dfpsf_p90)
    st.markdown(f"### {type}")
    # if counter % 2 == 0:

    st.markdown(f"#### No. of units sold per year")
    st.dataframe(dftown_txns.transpose())
    col1, col2 = st.columns(2)
    col1.markdown(f"#### Price trends")
    col1.line_chart(dftown_agg, x="year_of_sale")
    col2.markdown(f"#### PSF trends")
    col2.line_chart(dfpsf_agg, x="year_of_sale")
    # elif counter % 2 == 1:
    #     col2.markdown(f"#### {type}")
    #     col2.markdown(f"*No. of units sold per year*")
    #     col2.write(dftown_txns.transpose())
    #     col2.markdown(f"*Price Trends*")
    #     col2.line_chart(dftown_agg, x="year_of_sale")
    #     col2.line_chart(dfpsf_agg, x="year_of_sale")
    # counter += 1
