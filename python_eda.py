
from pathlib import Path

import pandas as pd
import numpy as np

# File paths
DATA_PATH = Path("data/processed/superstore_cleaned.csv")
OUTPUT_DIR = Path("outputs/tables")

try:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found: {DATA_PATH.resolve()}"
        )

    # 1. Load cleaned dataset
    df = pd.read_csv(DATA_PATH)

    # 2. Convert date columns
    for col in ["Order Date", "Ship Date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # 3. Ensure numeric columns have numeric data types
    numeric_columns = ["Sales", "Quantity", "Discount", "Profit"]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if df[numeric_columns].isnull().any().any():
        raise ValueError("Missing or invalid numeric values found.")

    if df[["Order Date", "Ship Date"]].isnull().any().any():
        raise ValueError("Invalid dates found in the dataset.")

    # 4. Overall business KPIs
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_quantity = df["Quantity"].sum()
    total_orders = df["Order ID"].nunique()

    average_order_value = (
        total_sales / total_orders if total_orders else np.nan
    )

    profit_margin = (
        np.divide(total_profit, total_sales) * 100
        if total_sales != 0 else np.nan
    )

    print("=" * 55)
    print("OVERALL BUSINESS KPIs")
    print("=" * 55)
    print(f"Dataset rows       : {len(df):,}")
    print(f"Total sales        : ${total_sales:,.2f}")
    print(f"Total profit       : ${total_profit:,.2f}")
    print(f"Total quantity     : {total_quantity:,}")
    print(f"Unique orders      : {total_orders:,}")
    print(f"Average order value: ${average_order_value:,.2f}")
    print(f"Profit margin      : {profit_margin:.2f}%")

    # 5. Category analysis
    category_summary = (
        df.groupby("Category", as_index=False)
        .agg(
            total_sales=("Sales", "sum"),
            total_profit=("Profit", "sum"),
            quantity_sold=("Quantity", "sum")
        )
        .sort_values("total_sales", ascending=False)
    )

    print("\nCATEGORY PERFORMANCE")
    print(category_summary.round(2).to_string(index=False))

    # 6. Regional analysis
    region_summary = (
        df.groupby("Region", as_index=False)
        .agg(
            total_sales=("Sales", "sum"),
            total_profit=("Profit", "sum")
        )
        .sort_values("total_profit", ascending=False)
    )

    print("\nREGION PERFORMANCE")
    print(region_summary.round(2).to_string(index=False))

    # 7. Monthly trend
    df["Sales Month"] = df["Order Date"].dt.to_period("M").astype(str)

    monthly_summary = (
        df.groupby("Sales Month", as_index=False)
        .agg(
            monthly_sales=("Sales", "sum"),
            monthly_profit=("Profit", "sum"),
            order_count=("Order ID", "nunique")
        )
        .sort_values("Sales Month")
    )

    print("\nFIRST 12 MONTHLY RECORDS")
    print(monthly_summary.head(12).round(2).to_string(index=False))

    # 8. Top 10 products by sales
    product_summary = (
        df.groupby("Product Name", as_index=False)
        .agg(
            total_sales=("Sales", "sum"),
            total_profit=("Profit", "sum")
        )
        .sort_values("total_sales", ascending=False)
        .head(10)
    )

    print("\nTOP 10 PRODUCTS BY SALES")
    print(product_summary.round(2).to_string(index=False))

    # 9. Loss-making sub-categories
    subcategory_summary = (
        df.groupby("Sub-Category", as_index=False)
        .agg(
            total_sales=("Sales", "sum"),
            total_profit=("Profit", "sum")
        )
        .sort_values("total_profit")
    )

    loss_making = subcategory_summary[
        subcategory_summary["total_profit"] < 0
    ]

    print("\nLOSS-MAKING SUB-CATEGORIES")
    print(loss_making.round(2).to_string(index=False))

    # 10. Discount analysis
    discount_summary = (
        df.groupby("Discount", as_index=False)
        .agg(
            transaction_lines=("Profit", "size"),
            average_profit=("Profit", "mean"),
            total_profit=("Profit", "sum"),
            total_sales=("Sales", "sum")
        )
        .sort_values("Discount")
    )

    print("\nDISCOUNT VS PROFIT")
    print(discount_summary.round(2).to_string(index=False))

    # 11. Save analysis tables
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    category_summary.to_csv(
        OUTPUT_DIR / "category_summary.csv", index=False
    )
    region_summary.to_csv(
        OUTPUT_DIR / "region_summary.csv", index=False
    )
    monthly_summary.to_csv(
        OUTPUT_DIR / "monthly_summary.csv", index=False
    )
    product_summary.to_csv(
        OUTPUT_DIR / "top_10_products.csv", index=False
    )
    loss_making.to_csv(
        OUTPUT_DIR / "loss_making_subcategories.csv", index=False
    )
    discount_summary.to_csv(
        OUTPUT_DIR / "discount_summary.csv", index=False
    )

    print("\nEDA completed successfully!")
    print("Summary tables saved to:", OUTPUT_DIR.resolve())

except FileNotFoundError as error:
    print("File error:", error)

except (ValueError, TypeError) as error:
    print("Data validation error:", error)

except Exception as error:
    print("Unexpected error:", error)
