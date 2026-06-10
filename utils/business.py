import altair as alt
import pandas as pd


LOW_STOCK_LIMIT = 20


def season_for_month(month: int) -> str:
    if month in (3, 4, 5):
        return "Summer"
    if month in (6, 7, 8, 9):
        return "Monsoon"
    if month in (10, 11):
        return "Festival"
    return "Winter"


def add_time_columns(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()
    enriched["season"] = enriched["date"].dt.month.apply(season_for_month)
    enriched["week"] = enriched["date"].dt.to_period("W").astype(str)
    enriched["month"] = enriched["date"].dt.to_period("M").astype(str)
    enriched["year"] = enriched["date"].dt.year.astype(str)
    return enriched


def seasonal_demand(df: pd.DataFrame, season: str | None = None) -> pd.DataFrame:
    enriched = add_time_columns(df)
    if season:
        enriched = enriched[enriched["season"] == season]

    return (
        enriched.groupby("product", as_index=False)
        .agg(units_sold=("units_sold", "sum"), revenue=("revenue", "sum"), stock=("stock", "last"))
        .sort_values("units_sold", ascending=False)
    )


def stock_status(df: pd.DataFrame, low_stock_limit: int = LOW_STOCK_LIMIT) -> pd.DataFrame:
    demand = (
        df.groupby("product", as_index=False)
        .agg(
            category=("category", "last"),
            units_sold=("units_sold", "sum"),
            revenue=("revenue", "sum"),
            stock=("stock", "last"),
        )
        .sort_values("stock")
    )
    demand["status"] = demand["stock"].apply(
        lambda value: "Low stock" if value <= low_stock_limit else "Healthy"
    )
    demand["reorder_units"] = demand["stock"].apply(
        lambda value: max(0, int(low_stock_limit * 2 - value))
    )
    return demand


def period_report(df: pd.DataFrame, period: str) -> pd.DataFrame:
    period_column = {"Weekly": "week", "Monthly": "month", "Yearly": "year"}[period]
    enriched = add_time_columns(df)
    return (
        enriched.groupby(period_column, as_index=False)
        .agg(units_sold=("units_sold", "sum"), revenue=("revenue", "sum"), stock=("stock", "last"))
        .rename(columns={period_column: "period"})
        .sort_values("period")
    )


def donut_chart(df: pd.DataFrame, label_column: str, value_column: str, title: str):
    return (
        alt.Chart(df, title=title)
        .mark_arc(innerRadius=55, outerRadius=115)
        .encode(
            theta=alt.Theta(field=value_column, type="quantitative"),
            color=alt.Color(field=label_column, type="nominal", legend=alt.Legend(title=None)),
            tooltip=[
                alt.Tooltip(field=label_column, type="nominal", title="Name"),
                alt.Tooltip(field=value_column, type="quantitative", title="Value", format=",.0f"),
            ],
        )
        .properties(height=320)
    )
