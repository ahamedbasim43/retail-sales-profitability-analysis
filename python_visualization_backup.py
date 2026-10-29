
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mtick

# ==========================================
# 1. LOAD DATA
# ==========================================

df = pd.read_csv("data/processed/superstore_cleaned.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"])

output_folder = "outputs/charts"
os.makedirs(output_folder, exist_ok=True)

sns.set_theme(style="whitegrid")

# ==========================================
# 2. PREPARE DATA
# ==========================================

total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_orders = df["Order ID"].nunique()
profit_margin = (total_profit / total_sales) * 100

category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

region_profit = (
    df.groupby("Region")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

monthly_sales = df.groupby(
    df["Order Date"].dt.to_period("M")
)["Sales"].sum()

monthly_sales.index = monthly_sales.index.to_timestamp()

discount_profit = (
    df.groupby("Discount", as_index=False)["Profit"]
    .mean()
)

# ==========================================
# 3. CREATE DASHBOARD LAYOUT
# ==========================================

fig = plt.figure(figsize=(18, 14), layout="constrained")

gs = fig.add_gridspec(
    3, 4,
    height_ratios=[0.8, 2, 2]
)

fig.suptitle(
    "RETAIL SALES & PROFITABILITY DASHBOARD",
    fontsize=20,
    fontweight="bold"
)

# ==========================================
# 4. KPI CARDS
# ==========================================

kpi_titles = [
    "TOTAL SALES",
    "TOTAL PROFIT",
    "TOTAL ORDERS",
    "PROFIT MARGIN"
]

kpi_values = [
    f"${total_sales:,.2f}",
    f"${total_profit:,.2f}",
    f"{total_orders:,}",
    f"{profit_margin:.2f}%"
]

for i in range(4):
    kpi_ax = fig.add_subplot(gs[0, i])
    kpi_ax.set_facecolor("#EAF2F8")
    kpi_ax.text(
        0.5, 0.65, kpi_titles[i],
        ha="center", va="center",
        fontsize=11, fontweight="bold",
        transform=kpi_ax.transAxes
    )
    kpi_ax.text(
        0.5, 0.32, kpi_values[i],
        ha="center", va="center",
        fontsize=17, fontweight="bold",
        transform=kpi_ax.transAxes
    )
    kpi_ax.set_xticks([])
    kpi_ax.set_yticks([])

    for spine in kpi_ax.spines.values():
        spine.set_visible(False)

# Chart locations
ax1 = fig.add_subplot(gs[1, 0:2])
ax2 = fig.add_subplot(gs[1, 2:4])
ax3 = fig.add_subplot(gs[2, 0:2])
ax4 = fig.add_subplot(gs[2, 2:4])

# ==========================================
# 5. CHART 1: CATEGORY-WISE SALES
# ==========================================

sns.barplot(
    x=category_sales.index,
    y=category_sales.values,
    ax=ax1
)

ax1.set_title("1. Total Sales by Product Category", fontsize=13)
ax1.set_xlabel("Product Category")
ax1.set_ylabel("Total Sales ($)")
ax1.yaxis.set_major_formatter(
    mtick.StrMethodFormatter("${x:,.0f}")
)

for container in ax1.containers:
    ax1.bar_label(
        container, fmt="$%.0f",
        padding=3, fontsize=9
    )

# ==========================================
# 6. CHART 2: REGION-WISE PROFIT
# ==========================================

sns.barplot(
    x=region_profit.index,
    y=region_profit.values,
    ax=ax2
)

ax2.set_title("2. Total Profit by Region", fontsize=13)
ax2.set_xlabel("Sales Region")
ax2.set_ylabel("Total Profit ($)")
ax2.yaxis.set_major_formatter(
    mtick.StrMethodFormatter("${x:,.0f}")
)

for container in ax2.containers:
    ax2.bar_label(
        container, fmt="$%.0f",
        padding=3, fontsize=9
    )

# ==========================================
# 7. CHART 3: MONTHLY SALES TREND
# ==========================================

sns.lineplot(
    x=monthly_sales.index,
    y=monthly_sales.values,
    marker="o",
    ax=ax3
)

ax3.set_title("3. Monthly Sales Trend (2014–2017)", fontsize=13)
ax3.set_xlabel("Order Month")
ax3.set_ylabel("Monthly Sales ($)")
ax3.yaxis.set_major_formatter(
    mtick.StrMethodFormatter("${x:,.0f}")
)

# Label every third month to avoid crowding
for i in range(0, len(monthly_sales), 3):
    date = monthly_sales.index[i]
    value = monthly_sales.iloc[i]

    ax3.annotate(
        f"${value:,.0f}",
        (date, value),
        textcoords="offset points",
        xytext=(0, 7),
        ha="center",
        fontsize=7
    )

ax3.tick_params(axis="x", rotation=45)

# ==========================================
# 8. CHART 4: DISCOUNT VS AVERAGE PROFIT
# ==========================================

sns.barplot(
    data=discount_profit,
    x="Discount",
    y="Profit",
    ax=ax4
)

ax4.axhline(
    y=0,
    color="black",
    linestyle="--",
    linewidth=1
)

ax4.set_title("4. Average Profit/Loss by Discount", fontsize=13)
ax4.set_xlabel("Discount Category")
ax4.set_ylabel("Average Profit/Loss ($)")

ax4.set_xticks(range(len(discount_profit)))
ax4.set_xticklabels(
    [f"{value:.0%}" for value in discount_profit["Discount"]]
)

for container in ax4.containers:
    labels = [
        f"${bar.get_height():,.0f}"
        for bar in container
    ]

    ax4.bar_label(
        container,
        labels=labels,
        padding=3,
        fontsize=7
    )

profit_min = discount_profit["Profit"].min()
profit_max = discount_profit["Profit"].max()

ax4.set_ylim(profit_min - 65, profit_max + 45)

# ==========================================
# 9. SAVE AND DISPLAY DASHBOARD
# ==========================================

dashboard_path = os.path.join(
    output_folder,
    "all_charts_dashboard.png"
)

fig.savefig(
    dashboard_path,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close(fig)

print("Dashboard created successfully!")
print("Total Sales:", f"${total_sales:,.2f}")
print("Total Profit:", f"${total_profit:,.2f}")
print("Total Orders:", f"{total_orders:,}")
print("Profit Margin:", f"{profit_margin:.2f}%")
print("Saved at:", dashboard_path)
