
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mdates
import seaborn as sns

# ==================================================
# 1. LOAD DATA
# ==================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "superstore_cleaned.csv"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "outputs",
    "charts"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)
df["Order Date"] = pd.to_datetime(df["Order Date"])

sns.set_theme(style="whitegrid")

# ==================================================
# 2. CALCULATE KPIs AND CHART DATA
# ==================================================

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()

profit_margin = (total_profit / total_sales) * 100
avg_order_value = total_sales / total_orders

# Category sales
category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

# Regional profit
region_profit = (
    df.groupby("Region")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

# Monthly sales
monthly_sales = (
    df.set_index("Order Date")["Sales"]
    .resample("MS")
    .sum()
)

# Average profit by discount
discount_profit = (
    df.groupby("Discount")["Profit"]
    .mean()
    .sort_index()
)

# Highest sales month
peak_month = monthly_sales.idxmax()
peak_sales = monthly_sales.max()

# ==================================================
# 3. DASHBOARD LAYOUT
# ==================================================

fig = plt.figure(
    figsize=(16, 11),
    facecolor="#F3F6FA"
)

gs = fig.add_gridspec(
    nrows=3,
    ncols=4,
    height_ratios=[0.85, 2.2, 2.4],
    hspace=0.48,
    wspace=0.42
)

fig.suptitle(
    "RETAIL SALES & PROFITABILITY DASHBOARD",
    fontsize=22,
    fontweight="bold",
    color="#17324D",
    y=0.97
)

# ==================================================
# 4. KPI CARDS
# ==================================================

kpi_titles = [
    "TOTAL SALES",
    "TOTAL PROFIT",
    "TOTAL ORDERS",
    "PROFIT MARGIN"
]

kpi_values = [
    f"${total_sales:,.0f}",
    f"${total_profit:,.0f}",
    f"{total_orders:,}",
    f"{profit_margin:.2f}%"
]

kpi_colors = [
    "#2563EB",
    "#16803D",
    "#7C3AED",
    "#D97706"
]

for i in range(4):

    ax = fig.add_subplot(gs[0, i])

    ax.set_facecolor("white")
    ax.set_xticks([])
    ax.set_yticks([])

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.text(
        0.5,
        0.68,
        kpi_titles[i],
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
        color="#526579",
        transform=ax.transAxes
    )

    ax.text(
        0.5,
        0.29,
        kpi_values[i],
        ha="center",
        va="center",
        fontsize=18,
        fontweight="bold",
        color=kpi_colors[i],
        transform=ax.transAxes
    )

# ==================================================
# 5. CHART 1: SALES BY PRODUCT CATEGORY
# ==================================================

ax1 = fig.add_subplot(gs[1, 0:2])

category_colors = [
    "#2F6690",
    "#5B8DB8",
    "#A7C7E7"
]

bars1 = ax1.bar(
    category_sales.index,
    category_sales.values,
    color=category_colors[:len(category_sales)],
    width=0.65
)

ax1.set_title(
    "Sales by Product Category",
    fontsize=13,
    fontweight="bold",
    color="#17324D",
    pad=12
)

ax1.set_xlabel("")
ax1.set_ylabel("Total Sales ($)")

ax1.yaxis.set_major_formatter(
    mtick.StrMethodFormatter("${x:,.0f}")
)

ax1.bar_label(
    bars1,
    labels=[
        f"${value:,.0f}"
        for value in category_sales.values
    ],
    padding=4,
    fontsize=8
)

ax1.tick_params(axis="x", labelsize=9)
ax1.margins(y=0.18)

# ==================================================
# 6. CHART 2: PROFIT BY REGION
# ==================================================

ax2 = fig.add_subplot(gs[1, 2:4])

region_colors = [
    "#247A4B",
    "#55A477",
    "#91C7A3",
    "#C7E3D0"
]

bars2 = ax2.bar(
    region_profit.index,
    region_profit.values,
    color=region_colors[:len(region_profit)],
    width=0.65
)

ax2.set_title(
    "Profit by Region",
    fontsize=13,
    fontweight="bold",
    color="#17324D",
    pad=12
)

ax2.set_xlabel("")
ax2.set_ylabel("Total Profit ($)")

ax2.yaxis.set_major_formatter(
    mtick.StrMethodFormatter("${x:,.0f}")
)

ax2.bar_label(
    bars2,
    labels=[
        f"${value:,.0f}"
        for value in region_profit.values
    ],
    padding=4,
    fontsize=8
)

ax2.tick_params(axis="x", labelsize=9)
ax2.margins(y=0.18)

# ==================================================
# 7. CHART 3: MONTHLY SALES TREND
# ==================================================

ax3 = fig.add_subplot(gs[2, 0:2])

ax3.plot(
    monthly_sales.index,
    monthly_sales.values,
    color="#2563EB",
    linewidth=2.2,
    marker="o",
    markersize=3.5
)

# Highlight the peak month
ax3.scatter(
    peak_month,
    peak_sales,
    color="#DC2626",
    s=75,
    zorder=5
)

ax3.annotate(
    f"Peak: ${peak_sales:,.0f}",
    xy=(peak_month, peak_sales),
    xytext=(-8, 12),
    textcoords="offset points",
    ha="right",
    fontsize=9,
    fontweight="bold",
    color="#DC2626"
)

ax3.set_title(
    "Monthly Sales Trend",
    fontsize=13,
    fontweight="bold",
    color="#17324D",
    pad=12
)

ax3.set_xlabel("Order Month")
ax3.set_ylabel("Monthly Sales ($)")

ax3.yaxis.set_major_formatter(
    mtick.StrMethodFormatter("${x:,.0f}")
)

# Show date labels every six months
ax3.xaxis.set_major_locator(
    mdates.MonthLocator(interval=6)
)

ax3.xaxis.set_major_formatter(
    mdates.DateFormatter("%b %Y")
)

ax3.tick_params(
    axis="x",
    rotation=30,
    labelsize=8
)

ax3.margins(x=0.04, y=0.20)

# ==================================================
# 8. CHART 4: AVERAGE PROFIT BY DISCOUNT
# ==================================================

ax4 = fig.add_subplot(gs[2, 2:4])

discount_labels = [
    f"{value:.0%}"
    for value in discount_profit.index
]

discount_colors = [
    "#16803D" if value >= 0 else "#DC2626"
    for value in discount_profit.values
]

bars4 = ax4.bar(
    discount_labels,
    discount_profit.values,
    color=discount_colors,
    width=0.68
)

ax4.axhline(
    0,
    color="#374151",
    linestyle="--",
    linewidth=1.2
)

ax4.set_title(
    "Average Profit by Discount",
    fontsize=13,
    fontweight="bold",
    color="#17324D",
    pad=12
)

ax4.set_xlabel("Discount Level")
ax4.set_ylabel("Average Profit ($)")

ax4.yaxis.set_major_formatter(
    mtick.StrMethodFormatter("${x:,.0f}")
)

ax4.bar_label(
    bars4,
    labels=[
        f"${value:,.0f}"
        for value in discount_profit.values
    ],
    padding=3,
    fontsize=7
)

ax4.tick_params(axis="x", labelsize=8)
ax4.margins(y=0.22)

# ==================================================
# 9. SAVE AND DISPLAY DASHBOARD
# ==================================================

dashboard_path = os.path.join(
    OUTPUT_DIR,
    "all_charts_dashboard.png"
)

fig.subplots_adjust(
    left=0.09,
    right=0.97,
    top=0.90,
    bottom=0.09
)

fig.savefig(
    dashboard_path,
    dpi=250,
    facecolor=fig.get_facecolor(),
    bbox_inches="tight"
)

print("\nDashboard created successfully!")
print(f"Total Sales       : ${total_sales:,.2f}")
print(f"Total Profit      : ${total_profit:,.2f}")
print(f"Total Orders      : {total_orders:,}")
print(f"Profit Margin     : {profit_margin:.2f}%")
print(f"Average Order     : ${avg_order_value:,.2f}")
print(f"Saved at          : {dashboard_path}")

# Open the dashboard window
plt.show(block=True)

plt.close(fig)
