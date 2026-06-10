import streamlit as st

from utils.business import add_time_columns, donut_chart
from utils.forecast import daily_sales, product_demand
from utils.preprocess import load_sales_data


st.title("Exploratory Data Analysis")

df = load_sales_data()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Revenue by Category")
    st.bar_chart(df.groupby("category")["revenue"].sum())
with col2:
    st.subheader("Units by Region")
    st.bar_chart(df.groupby("region")["units_sold"].sum())

pie_col1, pie_col2 = st.columns(2)
with pie_col1:
    st.subheader("Category Revenue Share")
    category_revenue = df.groupby("category", as_index=False)["revenue"].sum()
    st.altair_chart(
        donut_chart(category_revenue, "category", "revenue", "Category Revenue Share"),
        use_container_width=True,
    )
with pie_col2:
    st.subheader("Season Units Share")
    season_units = add_time_columns(df).groupby("season", as_index=False)["units_sold"].sum()
    st.altair_chart(
        donut_chart(season_units, "season", "units_sold", "Season Units Share"),
        use_container_width=True,
    )

st.subheader("Daily Trend")
st.line_chart(daily_sales(df).set_index("date")["units_sold"])

st.subheader("Product Demand")
st.dataframe(product_demand(df), hide_index=True, width="stretch")
