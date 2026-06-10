import streamlit as st

from utils.business import stock_status
from utils.forecast import product_demand
from utils.preprocess import load_sales_data
from utils.train_model import MODEL_PATH, train_sales_model


st.title("Model Training")

st.write("Train a small Random Forest model from the built-in manual sales dataset.")

df = load_sales_data()
training_view = product_demand(df).set_index("product")[["units_sold", "stock"]]
stock = stock_status(df)

st.subheader("Training Data Signal")
st.bar_chart(training_view)

col1, col2 = st.columns(2)
col1.metric("Training Rows", f"{len(df):,}")
col2.metric("Low Stock Signals", len(stock[stock["status"] == "Low stock"]))

st.subheader("Feature Preview")
st.dataframe(
    stock[["product", "category", "units_sold", "stock", "status"]],
    hide_index=True,
    width="stretch",
)

if st.button("Train model"):
    try:
        model, score = train_sales_model()
        st.success(f"Model saved to {MODEL_PATH}")
        st.metric("Validation R2", f"{score:.2f}")
    except Exception as exc:
        st.error(f"Training failed: {exc}")
