import sys
import runpy
from pathlib import Path

import streamlit as st


PROJECT_DIR = Path(__file__).resolve().parent
sys.path = [str(PROJECT_DIR)] + [path for path in sys.path if path != str(PROJECT_DIR)]

from utils.business import stock_status
from utils.forecast import daily_sales, product_demand
from utils.preprocess import (
    REQUIRED_COLUMNS,
    SUPPORTED_UPLOAD_TYPES,
    clean_sales_data,
    dataset_source_label,
    load_sales_data,
    read_dataset_file,
    summarize_data,
)


st.set_page_config(page_title="Intelligent Sales", layout="wide")


def apply_theme():
    st.markdown(
        """
        <style>
        :root {
            --app-bg: #090f1f;
            --panel: #101827;
            --panel-soft: #151f32;
            --text: #eef4ff;
            --muted: #9fb0ca;
            --blue: #0284ff;
            --cyan: #22d3ee;
            --line: rgba(148, 163, 184, 0.22);
        }

        .stApp {
            background:
                radial-gradient(circle at 78% 8%, rgba(34, 211, 238, 0.18), transparent 32%),
                radial-gradient(circle at 20% 24%, rgba(59, 130, 246, 0.15), transparent 28%),
                var(--app-bg);
            color: var(--text);
        }

        section[data-testid="stSidebar"] {
            background: #eef3ff;
            border-right: 1px solid #d7deef;
        }

        section[data-testid="stSidebar"] * {
            color: #15213a !important;
        }

        section[data-testid="stSidebar"] [role="radiogroup"] label {
            border-radius: 6px;
            padding: 6px 10px;
            margin: 2px 0;
        }

        section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
            background: #dfe8ff;
        }

        .block-container {
            max-width: 1160px;
            padding-top: 2.2rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3, p, label, span {
            color: var(--text);
        }

        .hero {
            position: relative;
            overflow: hidden;
            padding: 30px 34px;
            border: 1px solid rgba(125, 211, 252, 0.35);
            border-radius: 8px;
            background:
                linear-gradient(100deg, rgba(37, 99, 235, 0.95), rgba(2, 132, 255, 0.96) 58%, rgba(14, 165, 233, 0.82)),
                linear-gradient(135deg, #1d4ed8, #0284c7);
            box-shadow: 0 18px 50px rgba(2, 132, 255, 0.18);
        }

        .hero:after {
            content: "";
            position: absolute;
            top: 28px;
            right: 34px;
            width: 230px;
            height: 2px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.85), transparent);
            box-shadow: 0 0 22px rgba(255,255,255,0.8);
        }

        .hero h1 {
            margin: 0 0 8px 0;
            font-size: 30px;
            line-height: 1.1;
            color: #ffffff;
            letter-spacing: 0;
        }

        .hero p {
            margin: 0;
            color: rgba(255,255,255,0.84);
            font-size: 14px;
        }

        .glass-panel {
            min-height: 190px;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 20px;
            background: rgba(16, 24, 39, 0.82);
            box-shadow: 0 14px 38px rgba(0,0,0,0.22);
        }

        .glass-panel h2 {
            margin: 0 0 10px 0;
            font-size: 22px;
            color: #f8fbff;
        }

        .glass-panel p, .glass-panel li {
            color: var(--muted);
            font-size: 14px;
        }

        .quick-list {
            margin: 0;
            padding-left: 18px;
        }

        .quick-list li {
            margin-bottom: 8px;
        }

        .feature-card {
            min-height: 126px;
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 18px;
            background: linear-gradient(135deg, #172338, #0f172a);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.08), 0 12px 28px rgba(0,0,0,0.18);
        }

        .feature-card h3 {
            margin: 0 0 8px 0;
            color: #ffffff;
            font-size: 16px;
        }

        .feature-card p {
            margin: 0;
            color: #cbd5e1;
            font-size: 13px;
        }

        .card-action div[data-testid="stButton"] > button {
            width: 100%;
            margin-top: 8px;
            background: #22d3ee;
            color: #082f49;
            border-color: rgba(34, 211, 238, 0.65);
            font-weight: 700;
        }

        div[data-testid="stMetric"] {
            border: 1px solid var(--line);
            border-radius: 8px;
            padding: 14px 16px;
            background: rgba(16, 24, 39, 0.86);
        }

        div[data-testid="stMetric"] * {
            color: #eef4ff !important;
        }

        div[data-testid="stDataFrame"], div[data-testid="stTable"] {
            border-radius: 8px;
            overflow: hidden;
        }

        .stButton > button, .stDownloadButton > button {
            border-radius: 6px;
            border: 1px solid rgba(125, 211, 252, 0.45);
            background: #0284ff;
            color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data
def get_default_data(source_name: str = "default"):
    return load_sales_data()


def get_data():
    if st.session_state.get("uploaded_sales_data") is not None:
        return load_sales_data()
    return get_default_data()


def handle_dataset_upload(uploaded_file):
    if uploaded_file is None:
        return

    try:
        raw_df = read_dataset_file(uploaded_file)
        cleaned_df = clean_sales_data(raw_df)
    except Exception as exc:
        st.session_state.pop("uploaded_sales_data", None)
        st.session_state.pop("uploaded_sales_raw_data", None)
        st.session_state.pop("uploaded_sales_file_name", None)
        st.error(f"Dataset upload failed: {exc}")
        st.caption("Required columns: " + ", ".join(sorted(REQUIRED_COLUMNS)))
        return

    st.session_state.uploaded_sales_data = cleaned_df
    st.session_state.uploaded_sales_raw_data = raw_df
    st.session_state.uploaded_sales_file_name = uploaded_file.name
    st.success(f"Uploaded {uploaded_file.name} successfully.")


def navigate_to(page_name: str):
    st.session_state.selected_page = page_name
    st.rerun()


def show_dashboard():
    df = get_data()
    summary = summarize_data(df)

    st.markdown(
        """
        <div class="hero">
            <h1>Intelligent Sales Forecasting System</h1>
            <p>AI-powered sales analytics, forecasting, and inventory optimization.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    welcome_col, quick_col = st.columns([1.35, 1])
    with welcome_col:
        st.markdown(
            """
            <div class="glass-panel">
                <h2>Welcome</h2>
                <p>
                    This platform helps you analyze sales data, visualize trends,
                    forecast future revenue, optimize inventory, and generate
                    useful business reports from the processed dataset.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with quick_col:
        st.markdown(
            """
            <div class="glass-panel">
                <h2>Quick Start</h2>
                <ol class="quick-list">
                    <li><b>Sales Dataset</b> - View manual sales data</li>
                    <li><b>Preprocessing</b> - Check cleaned data</li>
                    <li><b>EDA</b> - Explore insights and charts</li>
                    <li><b>Forecasting</b> - Predict sales</li>
                    <li><b>Reports</b> - Download report output</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    card1, card2, card3 = st.columns(3)
    with card1:
        st.markdown(
            """
            <div class="card-action">
            <div class="feature-card">
                <h3>Analytics</h3>
                <p>Interactive charts for revenue, regions, categories, and daily units sold.</p>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Analytics", key="go_analytics"):
            navigate_to("EDA")
    with card2:
        st.markdown(
            """
            <div class="card-action">
            <div class="feature-card">
                <h3>Forecasting</h3>
                <p>Moving-average sales forecasts to estimate upcoming demand.</p>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Forecasting", key="go_forecasting"):
            navigate_to("Forecasting")
    with card3:
        st.markdown(
            """
            <div class="card-action">
            <div class="feature-card">
                <h3>Inventory</h3>
                <p>Product stock visibility with low-stock status for fast decisions.</p>
            </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Inventory", key="go_inventory"):
            navigate_to("Inventory")

    st.write("")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Rows", f"{summary['rows']:,}")
    col2.metric("Revenue", f"Rs. {summary['revenue']:,.0f}")
    col3.metric("Units Sold", f"{summary['units']:,}")
    col4.metric("Products", f"{summary['products']:,}")

    stock = stock_status(df)
    low_stock = stock[stock["status"] == "Low stock"]
    if not low_stock.empty:
        st.warning(
            "Low stock alert: "
            + ", ".join(low_stock["product"].head(5).tolist())
            + ("..." if len(low_stock) > 5 else "")
        )

    left, right = st.columns([2, 1])

    with left:
        st.subheader("Daily Sales")
        chart_data = daily_sales(df).set_index("date")[["units_sold", "revenue"]]
        st.line_chart(chart_data)

    with right:
        st.subheader("Top Products")
        st.dataframe(
            product_demand(df)[["product", "units_sold", "revenue", "stock"]].head(8),
            hide_index=True,
            width="stretch",
        )

    st.subheader("Recent Sales")
    st.dataframe(df.sort_values("date", ascending=False).head(20), hide_index=True, width="stretch")


def run_project_page(page_file: str):
    runpy.run_path(str(PROJECT_DIR / "pages" / page_file), run_name="__main__")


with st.sidebar:
    pages = [
        "Dashboard",
        "Sales Dataset",
        "EDA",
        "Preprocessing",
        "Forecasting",
        "Inventory",
        "Reports",
        "Training",
    ]
    if "selected_page" not in st.session_state:
        st.session_state.selected_page = "Dashboard"
    if st.session_state.selected_page not in pages:
        st.session_state.selected_page = "Dashboard"

    st.title("Sales App")
    selected_page = st.radio(
        "Pages",
        pages,
        index=pages.index(st.session_state.selected_page),
    )
    st.session_state.selected_page = selected_page

    st.divider()
    st.subheader("Manual Dataset")
    uploaded_file = st.file_uploader(
        "Upload dataset",
        type=SUPPORTED_UPLOAD_TYPES,
        key="manual_dataset_upload",
        help="CSV, TSV, TXT, JSON, XLSX, or XLS with sales columns.",
    )
    handle_dataset_upload(uploaded_file)

    if st.session_state.get("uploaded_sales_data") is not None:
        uploaded_df = st.session_state.uploaded_sales_data
        st.caption(
            f"Active upload: {st.session_state.uploaded_sales_file_name} ({len(uploaded_df):,} rows)"
        )
        if st.button("Use default dataset"):
            st.session_state.pop("uploaded_sales_data", None)
            st.session_state.pop("uploaded_sales_raw_data", None)
            st.session_state.pop("uploaded_sales_file_name", None)
            st.rerun()
    else:
        st.caption("No upload selected. Default dataset is active.")

    st.divider()
    st.caption(f"Using {dataset_source_label().lower()}.")

PAGE_FILES = {
    "Sales Dataset": "data_upload.py",
    "EDA": "eda.py",
    "Preprocessing": "preprocessing.py",
    "Forecasting": "forecasting.py",
    "Inventory": "inventory.py",
    "Reports": "reports.py",
    "Training": "training.py",
}

if selected_page == "Dashboard":
    apply_theme()
    show_dashboard()
else:
    apply_theme()
    run_project_page(PAGE_FILES[selected_page])
