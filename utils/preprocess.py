from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = BASE_DIR / "datasets" / "sales_data.csv"

REQUIRED_COLUMNS = {
    "date",
    "product",
    "category",
    "region",
    "units_sold",
    "unit_price",
    "stock",
}

SUPPORTED_UPLOAD_TYPES = ["csv", "tsv", "txt", "json", "xlsx", "xls"]


def read_dataset_file(uploaded_file) -> pd.DataFrame:
    file_name = getattr(uploaded_file, "name", "")
    suffix = Path(file_name).suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(uploaded_file)
    if suffix in {".tsv", ".txt"}:
        return pd.read_csv(uploaded_file, sep=None, engine="python")
    if suffix == ".json":
        return pd.read_json(uploaded_file)
    if suffix in {".xlsx", ".xls"}:
        try:
            return pd.read_excel(uploaded_file)
        except ImportError as exc:
            raise ImportError(
                "Excel upload needs openpyxl. Please install openpyxl or upload CSV/JSON."
            ) from exc

    raise ValueError("Unsupported file type. Upload CSV, TSV, TXT, JSON, XLSX, or XLS.")


def active_uploaded_data() -> pd.DataFrame | None:
    try:
        import streamlit as st
    except Exception:
        return None

    uploaded_df = st.session_state.get("uploaded_sales_data")
    if uploaded_df is None:
        return None
    return uploaded_df.copy()


def load_sales_data(uploaded_file=None) -> pd.DataFrame:
    if uploaded_file is not None:
        df = read_dataset_file(uploaded_file)
        return clean_sales_data(df)

    uploaded_df = active_uploaded_data()
    if uploaded_df is not None:
        return uploaded_df

    df = pd.read_csv(DEFAULT_DATASET)
    return clean_sales_data(df)


def load_raw_sales_data() -> pd.DataFrame:
    try:
        import streamlit as st
    except Exception:
        return pd.read_csv(DEFAULT_DATASET)

    uploaded_raw_df = st.session_state.get("uploaded_sales_raw_data")
    if uploaded_raw_df is not None:
        return uploaded_raw_df.copy()
    return pd.read_csv(DEFAULT_DATASET)


def load_selected_sales_data() -> pd.DataFrame:
    return load_sales_data()


def dataset_source_label() -> str:
    try:
        import streamlit as st
    except Exception:
        return "Default CSV -> processed cleaned dataset"

    uploaded_name = st.session_state.get("uploaded_sales_file_name")
    if uploaded_name:
        return f"Uploaded dataset ({uploaded_name}) -> processed cleaned dataset"
    return "Default CSV -> processed cleaned dataset"


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]

    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["units_sold"] = pd.to_numeric(df["units_sold"], errors="coerce").fillna(0)
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(0)
    df["stock"] = pd.to_numeric(df["stock"], errors="coerce").fillna(0)
    df = df.dropna(subset=["date", "product"]).drop_duplicates().sort_values("date")
    df["revenue"] = df["units_sold"] * df["unit_price"]
    return df


def summarize_data(df: pd.DataFrame) -> dict:
    return {
        "rows": len(df),
        "revenue": float(df["revenue"].sum()),
        "units": int(df["units_sold"].sum()),
        "products": int(df["product"].nunique()),
    }
