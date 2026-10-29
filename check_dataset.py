
from pathlib import Path
import pandas as pd
import numpy as np

# File paths
input_path = Path(r"E:\vs\super store.csv")
output_path = Path("data/processed/superstore_cleaned.csv")

try:
    # 1. Load original dataset
    df = pd.read_csv(input_path, encoding="cp1252")

    print("Original shape:", df.shape)

    # 2. Check missing values
    print("\nMissing values before cleaning:")
    print(df.isnull().sum().sum())

    # 3. Check exact duplicate rows
    print("\nExact duplicate rows:", df.duplicated().sum())

    # Remove only exact full-row duplicates, if any.
    # Valid order lines are not removed.
    df = df.drop_duplicates().copy()

    # 4. Convert dates.
    # This dataset uses US-style month/day/year dates.
    for col in ["Order Date", "Ship Date"]:
        df[col] = pd.to_datetime(
            df[col],
            format="mixed",
            dayfirst=False,
            errors="coerce"
        )

    # Check whether any dates failed to parse
    print("\nInvalid or unparsed dates:")
    print(df[["Order Date", "Ship Date"]].isnull().sum())

    # 5. Validate numeric columns
    numeric_columns = [
        "Row ID", "Sales", "Quantity", "Discount", "Profit"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    print("\nMissing values after type conversion:")
    print(df.isnull().sum()[df.isnull().sum() > 0])

    # 6. Validate logical conditions
    print("\nNon-positive quantity rows:", (df["Quantity"] <= 0).sum())
    print("Negative sales rows:", (df["Sales"] < 0).sum())
    print(
        "Discount outside 0-1:",
        ((df["Discount"] < 0) | (df["Discount"] > 1)).sum()
    )

    # 7. Save cleaned dataset
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print("\nCleaned shape:", df.shape)
    print("Cleaned dataset saved to:", output_path.resolve())
    print("\nDate data types:")
    print(df[["Order Date", "Ship Date"]].dtypes)

except FileNotFoundError:
    print("Input CSV not found. Check the file path:", input_path)

except Exception as error:
    print("An error occurred:", error)
