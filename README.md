# Intelligent Sales Forecasting System

AI-powered Streamlit dashboard for sales analytics, forecasting, inventory tracking, and reports using a built-in or manually uploaded sales dataset.

## Dashboard Preview

![Intelligent Sales Dashboard](assets/dashboard-screenshot.png)

## Features

- Sales dashboard with revenue and unit metrics
- Manual dataset upload from the sidebar
- Built-in processed sales dataset view
- Exploratory data analysis charts
- Preprocessing view for cleaned data
- Season-wise sales forecasting graphs
- Inventory stock visualization with low-stock alerts
- Weekly, monthly, and yearly reports with chart views
- Model training page

## Run Locally

```powershell
git clone https://github.com/LikithaNandini2006/intelligent-sales-forecasting-system.git
cd intelligent-sales-forecasting-system
python -m venv venv
venv\Scripts\pip install -r requirements.txt
venv\Scripts\streamlit run app.py
```

The app also works with the built-in dataset if you do not upload a file. Uploaded datasets should include these columns:

`date, product, category, region, units_sold, unit_price, stock`

## Project Structure

```text
intelligent sales/
  app.py
  requirements.txt
  README.md
  assets/
    dashboard-screenshot.png
  datasets/
    sales_data.csv
  pages/
    data_upload.py
    eda.py
    forecasting.py
    inventory.py
    preprocessing.py
    reports.py
    training.py
  utils/
    forecast.py
    preprocess.py
    train_model.py
```
