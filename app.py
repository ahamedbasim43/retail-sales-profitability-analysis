
import os
import pandas as pd
import streamlit as st
import plotly.express as px

# =========================================
# 1. PAGE CONFIGURATION
# =========================================

st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================
# 2. CUSTOM CSS
# =========================================

st.markdown("""
<style>

/* Overall font and background */
html, body, [class*="st-"] {
    font-family: "Segoe UI", Arial, sans-serif;
}

.stApp {
    background-color: #0B1120;
    color: #F1F5F9;
}

/* Main title */
h1 {
    color: #F8FAFC !important;
    font-size: 36px !important;
    font-weight: 750 !important;
    letter-spacing: -0.7px;
}

/* Section headings */
h2, h3 {
    color: #E2E8F0 !important;
    font-weight: 650 !important;
}

/* Description */
p {
    color: #CBD5E1;
    font-size: 14px;
}

/* KPI cards ONLY */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #172033, #111827);
    border: 1px solid #34445D;
    border-radius: 14px;
    padding: 20px 14px;
    min-height: 120px;
    width: 100%;
    box-sizing: border-box;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.18);
}

/* KPI labels */
div[data-testid="stMetricLabel"] {
    color: #A5B4FC !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

/* KPI values */
div[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: clamp(18px, 1.7vw, 27px) !important;
    font-weight: 700 !important;
    white-space: nowrap;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #171C2B;
    border-right: 1px solid #30384A;
}

/* Sidebar header */
section[data-testid="stSidebar"] h2 {
    color: #F8FAFC !important;
    font-size: 21px !important;
}

/* Divider */
hr {
    border-color: #30394A;
}

/* Remove chart container styling.
   No extra chart border, background, padding or shadow. */
div[data-testid="stPlotlyChart"] {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    box-shadow: none !important;
}

/* Buttons */
.stDownloadButton button {
    background-color: #3346A8;
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
}

.stDownloadButton button:hover {
    background-color: #4358C5;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# 3. LOAD DATA
# =========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "superstore_cleaned.csv"
)


@st.cache_data
def load_data(path):
    data = pd.read_csv(path)
    data["Order Date"] = pd.to_datetime(
        data["Order Date"], errors="coerce"
    )
    data = data.dropna(subset=["Order Date"])
    return data


try:
    df = load_data(DATA_PATH)
except FileNotFoundError:
    st.error(f"Dataset not found: {DATA_PATH}")
    st.stop()

# =========================================
# 4. DASHBOARD HEADER
# =========================================

st.title("📊 Retail Sales & Profitability Dashboard")

st.caption(
    "Explore sales, profit, product categories and regional performance."
)

# =========================================
# 5. SIDEBAR FILTERS
# =========================================

st.sidebar.header("🔎 Dashboard Filters")

years = sorted(df["Order Date"].dt.year.unique().tolist())

selected_years = st.sidebar.multiselect(
    "Select Year",
    options=years,
    default=years
)

categories = sorted(df["Category"].dropna().unique().tolist())

selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=categories,
    default=categories
)

regions = sorted(df["Region"].dropna().unique().tolist())

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=regions,
    default=regions
)

# =========================================
# 6. FILTER DATA
# =========================================

filtered_df = df[
    df["Order Date"].dt.year.isin(selected_years)
    & df["Category"].isin(selected_categories)
    & df["Region"].isin(selected_regions)
].copy()

if filtered_df.empty:
    st.warning(
        "No records match these filters. Please change your selection."
    )
    st.stop()

# =========================================
# 7. KPI CALCULATIONS
# =========================================

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0 else 0
)

avg_order_value = (
    total_sales / total_orders
    if total_orders != 0 else 0
)

# =========================================
# 8. KPI CARDS
# =========================================

col1, col2, col3, col4, col5 = st.columns(
    5,
    gap="medium"
)

with col1:
    st.metric(
        label="Total Sales",
        value=f"${total_sales:,.0f}"
    )

with col2:
    st.metric(
        label="Total Profit",
        value=f"${total_profit:,.0f}"
    )

with col3:
    st.metric(
        label="Unique Orders",
        value=f"{total_orders:,}"
    )

with col4:
    st.metric(
        label="Profit Margin",
        value=f"{profit_margin:.2f}%"
    )

with col5:
    st.metric(
        label="Average Order",
        value=f"${avg_order_value:,.2f}"
    )

st.divider()

# =========================================
# 9. SALES BY PRODUCT CATEGORY
# =========================================

left, right = st.columns(2, gap="large")

with left:
    st.subheader("Sales by Product Category")

    category_sales = (
        filtered_df.groupby("Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    fig_category = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        color="Category",
        text_auto=",.0f",
        title="Total Sales by Category",
        color_discrete_sequence=[
            "#6366F1", "#F97316", "#10B981"
        ]
    )

    fig_category.update_layout(
        template="plotly_dark",
        showlegend=False,
        yaxis_title="Sales ($)",
        xaxis_title="",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Segoe UI, Arial, sans-serif",
            size=12,
            color="#E2E8F0"
        ),
        title_font=dict(size=15, color="#F1F5F9"),
        margin=dict(l=8, r=8, t=55, b=8),
        autosize=True
    )

    fig_category.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True,
        config={"displaylogo": False, "responsive": True}
    )

# =========================================
# 10. PROFIT BY REGION
# =========================================

with right:
    st.subheader("Profit by Region")

    region_profit = (
        filtered_df.groupby("Region", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit", ascending=False)
    )

    fig_region = px.bar(
        region_profit,
        x="Region",
        y="Profit",
        color="Profit",
        color_continuous_scale="Greens",
        text_auto=",.0f",
        title="Total Profit by Region"
    )

    fig_region.update_layout(
        template="plotly_dark",
        coloraxis_showscale=False,
        yaxis_title="Profit ($)",
        xaxis_title="",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Segoe UI, Arial, sans-serif",
            size=12,
            color="#E2E8F0"
        ),
        title_font=dict(size=15, color="#F1F5F9"),
        margin=dict(l=8, r=8, t=55, b=8),
        autosize=True
    )

    fig_region.update_traces(
        textposition="outside",
        cliponaxis=False
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True,
        config={"displaylogo": False, "responsive": True}
    )

# =========================================
# 11. MONTHLY SALES TREND
# =========================================

st.subheader("Monthly Sales Trend")

monthly_sales = (
    filtered_df
    .set_index("Order Date")["Sales"]
    .resample("MS")
    .sum()
    .reset_index()
)

fig_monthly = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    markers=True,
    title="Monthly Sales Performance"
)

fig_monthly.update_layout(
    template="plotly_dark",
    xaxis_title="Month",
    yaxis_title="Sales ($)",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        family="Segoe UI, Arial, sans-serif",
        size=12,
        color="#E2E8F0"
    ),
    title_font=dict(size=15, color="#F1F5F9"),
    margin=dict(l=8, r=8, t=55, b=8),
    autosize=True
)

fig_monthly.update_traces(
    line=dict(color="#818CF8", width=3),
    marker=dict(size=6, color="#A5B4FC")
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True,
    config={"displaylogo": False, "responsive": True}
)

# =========================================
# 12. DISCOUNT VS AVERAGE PROFIT
# =========================================

st.subheader("Discount vs Average Profit")

discount_profit = (
    filtered_df.groupby("Discount", as_index=False)["Profit"]
    .mean()
    .sort_values("Discount")
)

discount_profit["Profit Status"] = discount_profit["Profit"].apply(
    lambda value: "Positive" if value >= 0 else "Negative"
)

fig_discount = px.bar(
    discount_profit,
    x="Discount",
    y="Profit",
    color="Profit Status",
    color_discrete_map={
        "Positive": "#22C55E",
        "Negative": "#EF4444"
    },
    text_auto=",.2f",
    title="Average Profit at Each Discount Level"
)

fig_discount.update_layout(
    template="plotly_dark",
    xaxis_title="Discount",
    yaxis_title="Average Profit ($)",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        family="Segoe UI, Arial, sans-serif",
        size=12,
        color="#E2E8F0"
    ),
    title_font=dict(size=15, color="#F1F5F9"),
    margin=dict(l=8, r=8, t=55, b=8),
    autosize=True
)

fig_discount.update_xaxes(tickformat=".0%")

st.plotly_chart(
    fig_discount,
    use_container_width=True,
    config={"displaylogo": False, "responsive": True}
)

# =========================================
# 13. FILTERED DATA TABLE & CSV DOWNLOAD
# =========================================

st.divider()

st.subheader("Filtered Sales Data")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data as CSV",
    data=csv_data,
    file_name="filtered_retail_sales.csv",
    mime="text/csv"
)

st.caption(
    f"Showing {len(filtered_df):,} records from the selected filters."
)
