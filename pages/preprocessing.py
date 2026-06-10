import streamlit as st

from utils.forecast import daily_sales
from utils.preprocess import dataset_source_label, load_raw_sales_data, load_sales_data


st.title("Preprocessing")

df = load_sales_data()
raw_df = load_raw_sales_data()

missing_values = int(raw_df.isna().sum().sum())
duplicate_rows = int(raw_df.duplicated().sum())

st.caption(f"Pipeline: {dataset_source_label()}.")

q1, q2, q3 = st.columns(3)
q1.metric("Raw Rows", f"{len(raw_df):,}")
q2.metric("Missing Values Fixed", f"{missing_values:,}")
q3.metric("Duplicate Rows Removed", f"{duplicate_rows:,}")

st.subheader("Cleaned Dataset")
st.write(f"Rows: {len(df):,} | Columns: {len(df.columns):,}")
st.dataframe(df, hide_index=True, width="stretch")

st.subheader("Cleaned Sales Trend")
st.line_chart(daily_sales(df).set_index("date")[["units_sold", "revenue"]])

st.subheader("Column Types")
st.dataframe(
    [{"column": column, "dtype": str(dtype)} for column, dtype in df.dtypes.items()],
    hide_index=True,
    width="stretch",
)
