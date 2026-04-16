import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ═══════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════
st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════
# CUSTOM STYLING
# ═══════════════════════════════════════════════
st.markdown("""
<style>
    .block-container { padding-top: 1.2rem; }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e3a5f11, #4a90d911);
        border: 1px solid #d6e4f0;
        border-radius: 10px;
        padding: 14px 18px;
    }
    [data-testid="stMetricLabel"] { font-size: 0.82rem; }
    [data-testid="stMetricValue"] { font-size: 1.5rem; font-weight: 700; }
    .sidebar-title { font-size: 1.2rem; font-weight: 700; margin-bottom: 0.4rem; }
    div[data-testid="stTabs"] button { font-size: 0.95rem; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("data/Sample - Superstore.csv", encoding="utf-8")

    # Parse dates
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="mixed", dayfirst=False)
    df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  format="mixed", dayfirst=False)

    # Derived columns
    df["Year"]       = df["Order Date"].dt.year
    df["Month"]      = df["Order Date"].dt.to_period("M").astype(str)
    df["Ship Days"]  = (df["Ship Date"] - df["Order Date"]).dt.days
    df["Profit Margin"] = (df["Profit"] / df["Sales"].replace(0, 1)) * 100

    return df

df = load_data()

# ═══════════════════════════════════════════════
# SIDEBAR FILTERS
# ═══════════════════════════════════════════════
st.sidebar.markdown('<p class="sidebar-title">🛒 Superstore Dashboard</p>', unsafe_allow_html=True)
st.sidebar.markdown("Use the filters below to explore the data.")
st.sidebar.markdown("---")

# Date range
min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()
date_range = st.sidebar.date_input(
    "📅 Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)
if isinstance(date_range, tuple) and len(date_range) == 2:
    date_from, date_to = date_range
else:
    date_from, date_to = min_date, max_date

# Region
all_regions = sorted(df["Region"].unique())
sel_regions = st.sidebar.multiselect("🌍 Region", all_regions, default=all_regions)

# Segment
all_segments = sorted(df["Segment"].unique())
sel_segments = st.sidebar.multiselect("👤 Segment", all_segments, default=all_segments)

# Category
all_categories = sorted(df["Category"].unique())
sel_categories = st.sidebar.multiselect("📦 Category", all_categories, default=all_categories)

# Ship Mode
all_ship = sorted(df["Ship Mode"].unique())
sel_ship = st.sidebar.multiselect("🚚 Ship Mode", all_ship, default=all_ship)

# ═══════════════════════════════════════════════
# APPLY FILTERS
# ═══════════════════════════════════════════════
mask = (
    (df["Order Date"].dt.date >= date_from)
    & (df["Order Date"].dt.date <= date_to)
    & (df["Region"].isin(sel_regions))
    & (df["Segment"].isin(sel_segments))
    & (df["Category"].isin(sel_categories))
    & (df["Ship Mode"].isin(sel_ship))
)
filtered = df[mask]

# ═══════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════
st.title("🛒 Superstore Sales Dashboard")
st.caption(
    f"Kaggle Sample Superstore · **{len(filtered):,}** orders "
    f"from **{date_from}** to **{date_to}**"
)

# ═══════════════════════════════════════════════
# KPI ROW
# ═══════════════════════════════════════════════
total_sales   = filtered["Sales"].sum()
total_profit  = filtered["Profit"].sum()
total_orders  = filtered["Order ID"].nunique()
avg_discount  = filtered["Discount"].mean() * 100
profit_margin = (total_profit / total_sales * 100) if total_sales else 0
avg_ship_days = filtered["Ship Days"].mean() if len(filtered) else 0

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("💰 Total Sales",      f"${total_sales:,.0f}")
k2.metric("📈 Total Profit",     f"${total_profit:,.0f}")
k3.metric("🛒 Unique Orders",    f"{total_orders:,}")
k4.metric("📊 Profit Margin",    f"{profit_margin:.1f}%")
k5.metric("🏷️ Avg Discount",     f"{avg_discount:.1f}%")
k6.metric("🚚 Avg Ship Days",    f"{avg_ship_days:.1f}")

st.markdown("---")

# ═══════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Sales Trends",
    "📦 Products",
    "🗺️ Regions",
    "👤 Customers",
    "📋 Raw Data",
])

PALETTE = ["#1e3a5f", "#4a90d9", "#50c878", "#f4a261", "#e76f51", "#9b59b6"]

# ─────────────────────────────────────────────
# TAB 1 — SALES TRENDS
# ─────────────────────────────────────────────
with tab1:
    monthly = (
        filtered.groupby("Month", as_index=False)
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
        .sort_values("Month")
    )

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Sales"],
        name="Sales", fill="tozeroy",
        line=dict(color=PALETTE[1], width=2),
    ))
    fig_trend.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Profit"],
        name="Profit", fill="tozeroy",
        line=dict(color=PALETTE[2], width=2),
    ))
    fig_trend.update_layout(
        title="Monthly Sales & Profit",
        xaxis_title="", yaxis_title="Amount ($)",
        plot_bgcolor="rgba(0,0,0,0)", yaxis_gridcolor="#eee",
        xaxis_tickangle=-45, legend=dict(orientation="h", y=1.08),
        margin=dict(t=55, b=50),
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        cat_monthly = (
            filtered.groupby(["Month", "Category"], as_index=False)["Sales"].sum()
            .sort_values("Month")
        )
        fig_cat_t = px.line(
            cat_monthly, x="Month", y="Sales", color="Category",
            title="Sales by Category Over Time", markers=True,
            color_discrete_sequence=PALETTE,
        )
        fig_cat_t.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", yaxis_gridcolor="#eee",
            xaxis_tickangle=-45, margin=dict(t=50, b=50),
            legend=dict(orientation="h", y=1.08),
        )
        st.plotly_chart(fig_cat_t, use_container_width=True)

    with c2:
        fig_orders = px.bar(
            monthly, x="Month", y="Orders",
            title="Monthly Order Count",
            color_discrete_sequence=[PALETTE[3]],
        )
        fig_orders.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", yaxis_gridcolor="#eee",
            xaxis_tickangle=-45, margin=dict(t=50, b=50),
        )
        st.plotly_chart(fig_orders, use_container_width=True)

# ─────────────────────────────────────────────
# TAB 2 — PRODUCTS
# ─────────────────────────────────────────────
with tab2:
    c1, c2 = st.columns(2)
    with c1:
        cat_sales = (
            filtered.groupby("Category", as_index=False)
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        )
        fig_cat = px.bar(
            cat_sales, x="Category", y=["Sales", "Profit"],
            title="Sales & Profit by Category", barmode="group",
            color_discrete_sequence=[PALETTE[1], PALETTE[2]],
        )
        fig_cat.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", yaxis_gridcolor="#eee",
            margin=dict(t=50), legend_title="",
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    with c2:
        sub_profit = (
            filtered.groupby("Sub-Category", as_index=False)["Profit"]
            .sum().sort_values("Profit", ascending=True).tail(10)
        )
        fig_sub = px.bar(
            sub_profit, x="Profit", y="Sub-Category", orientation="h",
            title="Top 10 Sub-Categories by Profit",
            color="Profit", color_continuous_scale="RdYlGn",
        )
        fig_sub.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", xaxis_gridcolor="#eee",
            margin=dict(t=50), coloraxis_showscale=False,
        )
        st.plotly_chart(fig_sub, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        sub_loss = (
            filtered.groupby("Sub-Category", as_index=False)["Profit"]
            .sum().sort_values("Profit").head(5)
        )
        fig_loss = px.bar(
            sub_loss, x="Sub-Category", y="Profit",
            title="⚠️ Bottom 5 Sub-Categories (Loss Makers)",
            color_discrete_sequence=["#e76f51"], text_auto="$.0f",
        )
        fig_loss.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", yaxis_gridcolor="#eee",
            margin=dict(t=50),
        )
        st.plotly_chart(fig_loss, use_container_width=True)

    with c4:
        fig_disc = px.scatter(
            filtered.sample(min(1000, len(filtered)), random_state=1),
            x="Discount", y="Profit", color="Category",
            title="Discount vs Profit", opacity=0.5,
            color_discrete_sequence=PALETTE,
        )
        fig_disc.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis_gridcolor="#eee", xaxis_gridcolor="#eee",
            margin=dict(t=50),
        )
        st.plotly_chart(fig_disc, use_container_width=True)

    top_prods = (
        filtered.groupby("Product Name", as_index=False)
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Qty=("Quantity", "sum"))
        .sort_values("Sales", ascending=False).head(10)
    )
    fig_top = px.bar(
        top_prods, x="Product Name", y="Sales",
        title="Top 10 Products by Sales",
        color="Profit", color_continuous_scale="RdYlGn", text_auto="$.0f",
    )
    fig_top.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", yaxis_gridcolor="#eee",
        xaxis_tickangle=-30, margin=dict(t=50, b=80),
        coloraxis_colorbar_title="Profit",
    )
    st.plotly_chart(fig_top, use_container_width=True)

# ─────────────────────────────────────────────
# TAB 3 — REGIONS
# ─────────────────────────────────────────────
with tab3:
    c1, c2 = st.columns(2)
    with c1:
        reg_data = (
            filtered.groupby("Region", as_index=False)
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        )
        fig_reg = px.bar(
            reg_data, x="Region", y=["Sales", "Profit"],
            title="Sales & Profit by Region", barmode="group",
            color_discrete_sequence=[PALETTE[1], PALETTE[2]], text_auto="$.0f",
        )
        fig_reg.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", yaxis_gridcolor="#eee",
            margin=dict(t=50), legend_title="",
        )
        st.plotly_chart(fig_reg, use_container_width=True)

    with c2:
        fig_pie = px.pie(
            reg_data, values="Sales", names="Region",
            title="Sales Share by Region",
            color_discrete_sequence=PALETTE, hole=0.4,
        )
        fig_pie.update_traces(textinfo="percent+label")
        fig_pie.update_layout(margin=dict(t=50))
        st.plotly_chart(fig_pie, use_container_width=True)

    heat = (
        filtered.groupby(["Region", "Category"], as_index=False)["Profit"]
        .sum().pivot(index="Region", columns="Category", values="Profit").fillna(0)
    )
    fig_heat = px.imshow(
        heat, text_auto="$.0f", title="Profit Heatmap: Region × Category",
        color_continuous_scale="RdYlGn",
        labels=dict(x="Category", y="Region", color="Profit ($)"),
    )
    fig_heat.update_layout(margin=dict(t=50))
    st.plotly_chart(fig_heat, use_container_width=True)

    state_data = (
        filtered.groupby("State", as_index=False)
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .sort_values("Sales", ascending=False).head(10)
    )
    fig_state = px.bar(
        state_data, x="State", y="Sales", color="Profit",
        title="Top 10 States by Sales",
        color_continuous_scale="RdYlGn", text_auto="$.0f",
    )
    fig_state.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", yaxis_gridcolor="#eee",
        margin=dict(t=50, b=50),
    )
    st.plotly_chart(fig_state, use_container_width=True)

# ─────────────────────────────────────────────
# TAB 4 — CUSTOMERS
# ─────────────────────────────────────────────
with tab4:
    c1, c2 = st.columns(2)
    with c1:
        seg_data = (
            filtered.groupby("Segment", as_index=False)
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
        )
        fig_seg = px.bar(
            seg_data, x="Segment", y=["Sales", "Profit"],
            title="Sales & Profit by Customer Segment", barmode="group",
            color_discrete_sequence=[PALETTE[1], PALETTE[2]],
        )
        fig_seg.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", yaxis_gridcolor="#eee",
            margin=dict(t=50), legend_title="",
        )
        st.plotly_chart(fig_seg, use_container_width=True)

    with c2:
        ship_data = filtered["Ship Mode"].value_counts().reset_index()
        ship_data.columns = ["Ship Mode", "Count"]
        fig_ship = px.pie(
            ship_data, values="Count", names="Ship Mode",
            title="Orders by Ship Mode",
            color_discrete_sequence=PALETTE, hole=0.4,
        )
        fig_ship.update_traces(textinfo="percent+label")
        fig_ship.update_layout(margin=dict(t=50))
        st.plotly_chart(fig_ship, use_container_width=True)

    top_cust = (
        filtered.groupby("Customer Name", as_index=False)
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
        .sort_values("Sales", ascending=False).head(10)
    )
    fig_cust = px.bar(
        top_cust, x="Customer Name", y="Sales",
        title="Top 10 Customers by Sales",
        color="Profit", color_continuous_scale="RdYlGn", text_auto="$.0f",
    )
    fig_cust.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", yaxis_gridcolor="#eee",
        xaxis_tickangle=-30, margin=dict(t=50, b=80),
    )
    st.plotly_chart(fig_cust, use_container_width=True)

# ─────────────────────────────────────────────
# TAB 5 — RAW DATA
# ─────────────────────────────────────────────
with tab5:
    st.subheader("Filtered Dataset")
    display_cols = [
        "Order ID", "Order Date", "Ship Mode", "Customer Name",
        "Segment", "Region", "State", "City",
        "Category", "Sub-Category", "Product Name",
        "Sales", "Quantity", "Discount", "Profit",
    ]
    st.dataframe(
        filtered[display_cols].reset_index(drop=True),
        use_container_width=True, height=500,
    )
    csv_bytes = filtered[display_cols].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇️ Download Filtered Data as CSV",
        data=csv_bytes,
        file_name="superstore_filtered.csv",
        mime="text/csv",
    )

# ═══════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════
st.markdown("---")
st.caption(
    "Built with Streamlit & Plotly · "
    "Data: [Kaggle Sample Superstore](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) · "
    "Module 6 Mini Project"
)
