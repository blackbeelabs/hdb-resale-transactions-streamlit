import streamlit as st

st.set_page_config(layout="wide")
import pandas as pd
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
df = pd.read_csv(
    os.path.join(PROJECT_DIR, "assets", "entity-transaction.csv"),
)

df_num_txns = df.groupby("year_of_sale").size().reset_index(name="Number of txns")
df_num_txns["Number of txns"] = df_num_txns["Number of txns"].astype(float)
df_num_txns.rename(columns={"year_of_sale": "year"}, inplace=True)
df_num_txns_txt = df_num_txns.copy()
df_num_txns_txt["year"] = df_num_txns_txt["year"].astype(str)
df_num_txns_txt["Number of txns"] = df_num_txns_txt["Number of txns"].apply(
    lambda x: f"{x:,.0f}"
)
df_num_txns_txt.rename(columns={"year": "Year"}, inplace=True)

df_avg_price = (
    df.groupby("year_of_sale")["price"].mean().reset_index(name="Average Price")
)
df_avg_price.rename(columns={"year_of_sale": "year"}, inplace=True)
df_avg_price_txt = df_avg_price.copy()
df_avg_price_txt["year"] = df_avg_price_txt["year"].astype(str)
df_avg_price_txt["Average Price"] = df_avg_price_txt["Average Price"].apply(
    lambda x: f"${x:,.0f}"
)
df_avg_price_txt.rename(columns={"year": "Year"}, inplace=True)

st.markdown("# Welcome!")
st.markdown(
    """Welcome to the HDB Resale Dashboard. This captures all transactions from 2014 to 2024 February.
    """
)
st.write(
    """Dataset credits from <a href="https://beta.data.gov.sg/collections/189/view" target="_blank" >data.gov.sg</a>""",
    unsafe_allow_html=True,
)
col1, col2 = st.columns(2)
col1.markdown("### Number of Transactions per year")
col1.dataframe(
    df_num_txns_txt.sort_values(
        "Year",
    ),
    hide_index=True,
    use_container_width=True,
)
col2.markdown("### Average Price per year")
col2.dataframe(
    df_avg_price_txt.sort_values(
        "Year",
    ),
    hide_index=True,
    use_container_width=True,
)
col1, col2 = st.columns(2)
col1.markdown("#### No. of Transactions per Year")
col1.line_chart(df_num_txns, x="year", y="Number of txns")
# For debugging
# col1.dataframe(df_num_txns)
# col1.write(df_num_txns.describe(include="all"))
# col1.write(df_num_txns.dtypes)

col2.markdown("#### Average Price by Year")
col2.line_chart(df_avg_price, x="year", y="Average Price")
# For debugging
# col2.dataframe(df_avg_price)
# col2.write(df_avg_price.describe(include="all"))
# col2.write(df_avg_price.dtypes)

st.write(
    """Built by <a href="https://twitter.com/bryanblackbee" target="_blank" >bryanblackbee</a>""",
    unsafe_allow_html=True,
)
