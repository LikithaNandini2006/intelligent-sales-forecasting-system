import streamlit as st

from utils.business import add_time_columns, donut_chart, seasonal_demand
from utils.forecast import moving_average_forecast
from utils.preprocess import load_sales_data


st.title("Sales Forecasting")

df = load_sales_data()

days = st.slider("Forecast days", min_value=3, max_value=30, value=7)
window = st.slider("Moving average window", min_value=3, max_value=14, value=7)

forecast = moving_average_forecast(df, days=days, window=window)

st.subheader("Forecast")
st.line_chart(forecast.set_index("date")[["forecast_units", "forecast_revenue"]])
st.dataframe(forecast, hide_index=True, width="stretch")

enriched = add_time_columns(df)
current_season = enriched.sort_values("date")["season"].iloc[-1]
season = st.selectbox(
    "Season demand view",
    ["All Seasons", "Summer", "Monsoon", "Festival", "Winter"],
    index=["All Seasons", "Summer", "Monsoon", "Festival", "Winter"].index(current_season),
)

season_demand = seasonal_demand(df, None if season == "All Seasons" else season)
high_demand = season_demand.head(1)
low_demand = season_demand.tail(1)

st.subheader("Season Demand")
if not high_demand.empty and not low_demand.empty:
    left, right = st.columns(2)
    left.metric("Highest Demand", high_demand.iloc[0]["product"], f"{int(high_demand.iloc[0]['units_sold'])} units")
    right.metric("Lowest Demand", low_demand.iloc[0]["product"], f"{int(low_demand.iloc[0]['units_sold'])} units")

st.altair_chart(
    donut_chart(season_demand, "product", "units_sold", f"{season} Product Demand Share"),
    use_container_width=True,
)
st.dataframe(season_demand, hide_index=True, width="stretch")
