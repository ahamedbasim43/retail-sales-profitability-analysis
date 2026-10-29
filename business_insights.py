
import os
import pandas as pd

# 1. Dataset path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(
    BASE_DIR, "data", "processed", "superstore_cleaned.csv"
)

# 2. Load data
df = pd.read_csv(DATA_PATH)
df["Order Date"] = pd.to_datetime(df["Order Date"])

# 3. Best category by sales
category_sales = df.groupby("Category")["Sales"].sum()
best_category = category_sales.idxmax()
best_sales = category_sales.max()

# 4. Biggest loss-making sub-category
subcategory_profit = df.groupby("Sub-Category")["Profit"].sum()
worst_subcategory = subcategory_profit.idxmin()
worst_profit = subcategory_profit.min()

# 5. Highest sales month
monthly_sales = (
    df.set_index("Order Date")["Sales"]
    .resample("MS")
    .sum()
)
peak_month = monthly_sales.idxmax()
peak_sales = monthly_sales.max()

# 6. Discount risk analysis
discount_profit = df.groupby("Discount")["Profit"].mean()
loss_discounts = discount_profit[discount_profit < 0]

# 7. Display insights
print("\n" + "=" * 50)
print("       RETAIL BUSINESS INSIGHTS")
print("=" * 50)

print("\n1. BEST SALES CATEGORY")
print(f"   Category: {best_category}")
print(f"   Total Sales: ${best_sales:,.2f}")

print("\n2. BIGGEST LOSS-MAKING SUB-CATEGORY")
print(f"   Sub-category: {worst_subcategory}")
print(f"   Total Profit: ${worst_profit:,.2f}")

print("\n3. HIGHEST SALES MONTH")
print(f"   Month: {peak_month.strftime('%B %Y')}")
print(f"   Sales: ${peak_sales:,.2f}")

print("\n4. DISCOUNT RISK")
if not loss_discounts.empty:
    print("   Discount levels with negative average profit:")
    for discount, profit in loss_discounts.items():
        print(
            f"   {discount:.0%} discount -> "
            f"Average Profit: ${profit:,.2f}"
        )
else:
    print("   No discount level has negative average profit.")

print("\n" + "=" * 50)
