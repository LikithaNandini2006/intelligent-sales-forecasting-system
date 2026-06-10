import pandas as pd


def daily_sales(df: pd.DataFrame) -> pd.DataFrame:
    sales = (
        df.groupby("date", as_index=False)
        .agg(units_sold=("units_sold", "sum"), revenue=("revenue", "sum"))
        .sort_values("date")
    )
    return sales


def moving_average_forecast(df: pd.DataFrame, days: int = 7, window: int = 7) -> pd.DataFrame:
    sales = daily_sales(df)
    if sales.empty:
        return pd.DataFrame(columns=["date", "forecast_units", "forecast_revenue"])

    avg_units = sales["units_sold"].tail(window).mean()
    avg_revenue = sales["revenue"].tail(window).mean()
    start = sales["date"].max() + pd.Timedelta(days=1)
    dates = pd.date_range(start=start, periods=days, freq="D")
    return pd.DataFrame(
        {
            "date": dates,
            "forecast_units": [round(avg_units, 2)] * days,
            "forecast_revenue": [round(avg_revenue, 2)] * days,
        }
    )


def product_demand(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("product", as_index=False)
        .agg(units_sold=("units_sold", "sum"), revenue=("revenue", "sum"), stock=("stock", "last"))
        .sort_values("units_sold", ascending=False)
    )
