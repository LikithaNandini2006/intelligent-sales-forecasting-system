import streamlit as st

from utils.business import LOW_STOCK_LIMIT, donut_chart, stock_status
from utils.preprocess import load_sales_data


st.title("Inventory")

df = load_sales_data()
demand = stock_status(df)

low_stock = demand[demand["status"] == "Low stock"]
healthy_stock = demand[demand["status"] == "Healthy"]

col1, col2, col3 = st.columns(3)
col1.metric("Total Products", len(demand))
col2.metric("Low Stock Products", len(low_stock))
col3.metric("Healthy Products", len(healthy_stock))

if not low_stock.empty:
    st.error(
        f"Low stock alert: {len(low_stock)} products are at or below {LOW_STOCK_LIMIT} units."
    )
    st.dataframe(
        low_stock[["product", "category", "stock", "units_sold", "reorder_units"]],
        hide_index=True,
        width="stretch",
    )
else:
    st.success("All products have healthy stock.")

st.subheader("Stock by Product")
st.bar_chart(demand.set_index("product")["stock"])

st.altair_chart(
    donut_chart(demand, "product", "stock", "Current Stock Share"),
    use_container_width=True,
)

st.subheader("Inventory Status")
st.dataframe(
    demand[["product", "category", "units_sold", "stock", "status", "reorder_units"]],
    hide_index=True,
    width="stretch",
)
