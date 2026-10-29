
import sqlite3
from pathlib import Path
import pandas as pd

db_path = Path("database/retail_sales.db")

queries = {
    "Overall Performance": """
        SELECT
            ROUND(SUM(Sales), 2) AS total_sales,
            ROUND(SUM(Profit), 2) AS total_profit,
            COUNT(DISTINCT "Order ID") AS total_orders
        FROM superstore;
    """,

    "Category Performance": """
        SELECT Category,
               ROUND(SUM(Sales), 2) AS total_sales,
               ROUND(SUM(Profit), 2) AS total_profit
        FROM superstore
        GROUP BY Category
        ORDER BY total_sales DESC;
    """,

    "Region Performance": """
        SELECT Region,
               ROUND(SUM(Sales), 2) AS total_sales,
               ROUND(SUM(Profit), 2) AS total_profit
        FROM superstore
        GROUP BY Region
        ORDER BY total_profit DESC;
    """,

    "Monthly Sales Trend": """
        SELECT strftime('%Y-%m', "Order Date") AS sales_month,
               ROUND(SUM(Sales), 2) AS monthly_sales,
               ROUND(SUM(Profit), 2) AS monthly_profit
        FROM superstore
        GROUP BY sales_month
        ORDER BY sales_month;
    """,

    "Top 10 Products": """
        SELECT "Product Name",
               ROUND(SUM(Sales), 2) AS total_sales,
               ROUND(SUM(Profit), 2) AS total_profit
        FROM superstore
        GROUP BY "Product Name"
        ORDER BY total_sales DESC
        LIMIT 10;
    """,

    "Loss-Making Sub-Categories": """
        SELECT "Sub-Category",
               ROUND(SUM(Sales), 2) AS total_sales,
               ROUND(SUM(Profit), 2) AS total_profit
        FROM superstore
        GROUP BY "Sub-Category"
        HAVING SUM(Profit) < 0
        ORDER BY total_profit ASC;
    """,

    "Discount vs Profit": """
        SELECT Discount,
               COUNT(*) AS transaction_lines,
               ROUND(AVG(Profit), 2) AS average_profit,
               ROUND(SUM(Profit), 2) AS total_profit,
               ROUND(SUM(Sales), 2) AS total_sales
        FROM superstore
        GROUP BY Discount
        ORDER BY Discount;
    """,

    "Monthly Order Count": """
        SELECT strftime('%Y-%m', "Order Date") AS sales_month,
               COUNT(DISTINCT "Order ID") AS total_orders,
               ROUND(AVG(Sales), 2) AS average_line_sales
        FROM superstore
        GROUP BY sales_month
        ORDER BY sales_month;
    """
}

try:
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")

    with sqlite3.connect(db_path) as connection:
        for title, query in queries.items():
            print(f"\n{'=' * 55}")
            print(title)
            print('=' * 55)

            result = pd.read_sql_query(query, connection)
            print(result.to_string(index=False))

except FileNotFoundError as error:
    print(error)

except Exception as error:
    print("SQL execution error:", error)
