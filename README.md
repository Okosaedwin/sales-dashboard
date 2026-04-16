# 🛒 Superstore Sales Dashboard

An interactive sales dashboard built with **Python**, **Streamlit**, and **Plotly** — powered by the Kaggle Sample Superstore dataset.

## Features

- **6 KPI Cards** — Total Sales, Profit, Orders, Profit Margin, Avg Discount, Avg Ship Days
- **5 Tabs** — Sales Trends, Products, Regions, Customers, Raw Data
- **Interactive Filters** — Date range, Region, Segment, Category, Ship Mode
- **15+ Charts** — Area, bar, line, pie, scatter, heatmap
- **CSV Export** — Download filtered data

## Dataset

This project uses the **Kaggle Sample Superstore** dataset.

### Option A — Use the included sample data (quickest)
The repo includes `generate_data.py` which creates a realistic 9,994-row CSV
matching the Kaggle schema. Just run:
```bash
python generate_data.py
```
This creates `data/Sample - Superstore.csv` automatically.

### Option B — Use the real Kaggle dataset (recommended)
1. Go to: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
2. Click **Download** (requires a free Kaggle account).
3. Extract the CSV and place it at: `data/Sample - Superstore.csv`

Both options produce the same column schema, so the dashboard works identically.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate sample data (skip if using the real Kaggle CSV)
python generate_data.py

# 3. Run the dashboard
streamlit run app.py
```
Opens at `http://localhost:8501`.

## Deploy to Streamlit Community Cloud

1. Push this folder to a **GitHub repository**.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app** → select your repo, branch, and `app.py`.
4. Click **Deploy**. Public URL ready in ~2 minutes.

> **Note:** Include `data/Sample - Superstore.csv` in your repo so the deployed
> app can load it. Alternatively, add `generate_data.py` to a setup script.

## Project Structure

```
sales-dashboard/
├── app.py                # Main dashboard (Streamlit + Plotly)
├── generate_data.py      # Generates sample CSV matching Kaggle schema
├── requirements.txt      # Python dependencies
├── README.md             # This file
└── data/
    └── Sample - Superstore.csv   # Dataset (generated or from Kaggle)
```
