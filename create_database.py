
from pathlib import Path
import sqlite3
import pandas as pd

# Project paths
data_path = Path("data/processed/superstore_cleaned.csv")
db_path = Path("database/retail_sales.db")

try:
    if not data_path.exists():
        raise FileNotFoundError(
            f"Cleaned dataset not found: {data_path}"
        )

    # Read cleaned dataset
    df = pd.read_csv(data_path)

    # Create database folder if needed
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Connect to SQLite database
    with sqlite3.connect(db_path) as connection:

        # Load data into SQL table
        df.to_sql(
            "superstore",
            connection,
            if_exists="replace",
            index=False
        )

        # Verify row count
        result = pd.read_sql_query(
            "SELECT COUNT(*) AS total_rows FROM superstore",
            connection
        )

        print("Database created successfully!")
        print("Database location:", db_path.resolve())
        print("\nSQL table row count:")
        print(result)

        # Preview SQL table
        preview = pd.read_sql_query(
            "SELECT * FROM superstore LIMIT 5",
            connection
        )

        print("\nFirst 5 SQL records:")
        print(preview)

except FileNotFoundError as error:
    print(error)

except Exception as error:
    print("Database creation error:", error)
