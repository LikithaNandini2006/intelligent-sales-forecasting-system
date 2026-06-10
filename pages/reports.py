import streamlit as st

from utils.business import donut_chart, period_report
from utils.forecast import moving_average_forecast, product_demand
from utils.preprocess import load_sales_data, summarize_data


st.title("Reports")

df = load_sales_data()
summary = summarize_data(df)
forecast = moving_average_forecast(df)
products = product_demand(df)

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"Rs. {summary['revenue']:,.0f}")
col2.metric("Total Units", f"{summary['units']:,}")
col3.metric("Products", f"{summary['products']:,}")

st.subheader("Product Revenue Graph")
st.bar_chart(products.set_index("product")["revenue"])

report_type = st.radio(
    "Report Period",
    ["Weekly", "Monthly", "Yearly"],
    index=0,
    horizontal=True,
)
period_data = period_report(df, report_type)

left, right = st.columns(2)
with left:
    st.subheader(f"{report_type} Revenue Share")
    st.altair_chart(
        donut_chart(period_data, "period", "revenue", f"{report_type} Revenue Share"),
        use_container_width=True,
    )
with right:
    st.subheader(f"{report_type} Units Share")
    st.altair_chart(
        donut_chart(period_data, "period", "units_sold", f"{report_type} Units Share"),
        use_container_width=True,
    )

st.subheader(f"{report_type} Report")
st.dataframe(period_data, hide_index=True, width="stretch")

st.subheader("Product Report")
st.dataframe(products, hide_index=True, width="stretch")

st.subheader("Forecast Report")
st.line_chart(forecast.set_index("date")[["forecast_units", "forecast_revenue"]])
st.dataframe(forecast, hide_index=True, width="stretch")

csv = forecast.to_csv(index=False).encode("utf-8")
st.download_button("Download forecast CSV", csv, "forecast_report.csv", "text/csv")
