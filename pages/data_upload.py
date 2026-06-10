import streamlit as st

from utils.forecast import daily_sales
from utils.preprocess import dataset_source_label, load_raw_sales_data, load_sales_data, summarize_data


st.title("Sales Dataset")

df = load_sales_data()
raw_df = load_raw_sales_data()

summary = summarize_data(df)

st.caption(f"Current source: {dataset_source_label()}.")

col_a, col_b, col_c = st.columns(3)
col_a.metric("Clean Rows", f"{summary['rows']:,}")
col_b.metric("Revenue", f"Rs. {summary['revenue']:,.0f}")
col_c.metric("Units Sold", f"{summary['units']:,}")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Units Sold Trend")
    st.line_chart(daily_sales(df).set_index("date")["units_sold"])
with col2:
    st.subheader("Revenue by Region")
    st.bar_chart(df.groupby("region")["revenue"].sum())

st.subheader("Processed Dataset")
st.dataframe(df, hide_index=True, width="stretch")

with st.expander("Raw default CSV preview"):
    st.dataframe(raw_df.head(20), hide_index=True, width="stretch")
