"""Data Cleaning Module.

This module handles data cleaning and preprocessing for customers and orders.
Performs operations like duplicate removal, data validation, and format standardization.
"""

import pandas as pd
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
RAW_DATA = BASE_DIR / "data" / "raw"
PROCESSED_DATA = BASE_DIR / "data" / "processed"

# Ensure processed data directory exists
PROCESSED_DATA.mkdir(parents=True, exist_ok=True)


def load_csv(file_path: str) -> pd.DataFrame:
    """Load CSV file into pandas DataFrame.

    Args:
        file_path: Path to CSV file to load.

    Returns:
        pd.DataFrame: Loaded data or None if file not found.

    Raises:
        FileNotFoundError: If CSV file doesn't exist.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        raise


# -------------------------
# Clean Customers Data
# -------------------------

def clean_customers() -> pd.DataFrame:
    """Clean and validate customer data.

    Operations:
    - Remove duplicate customer_id entries (keep latest signup_date)
    - Normalize emails to lowercase
    - Validate email format (must contain @ and .)
    - Parse signup_date to datetime format
    - Strip whitespace from name and region
    - Fill missing regions with 'Unknown'

    Returns:
        pd.DataFrame: Cleaned customer data.
    """
    df = load_csv(RAW_DATA / "customers.csv")

    print("\nCustomers BEFORE cleaning:", len(df), "rows")

    # remove duplicates
    df = df.sort_values("signup_date")
    df = df.drop_duplicates(subset="customer_id", keep="last")

    # lowercase emails
    df["email"] = df["email"].str.lower()

    # email validation
    df["is_valid_email"] = df["email"].str.contains("@") & df["email"].str.contains(".")

    # parse signup date
    df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")

    # strip whitespace
    df["name"] = df["name"].str.strip()
    df["region"] = df["region"].str.strip()

    # fill missing region
    df["region"] = df["region"].fillna("Unknown")

    print("Customers AFTER cleaning:", len(df), "rows")

    df.to_csv(PROCESSED_DATA / "customers_clean.csv", index=False)
    return df


# -------------------------
# Custom Date Parser
# -------------------------

def parse_date(val) -> pd.Timestamp:
    """Parse date string in multiple formats.

    Supports formats: YYYY-MM-DD, DD/MM/YYYY, MM-DD-YYYY.

    Args:
        val: Date string to parse.

    Returns:
        pd.Timestamp: Parsed datetime or NaT if unparseable.
    """
    formats = ["%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y"]

    for fmt in formats:
        try:
            return pd.to_datetime(val, format=fmt)
        except (ValueError, TypeError):
            continue

    return pd.NaT


# -------------------------
# Clean Orders Data
# -------------------------

def clean_orders() -> pd.DataFrame:
    """Clean and standardize order data.

    Operations:
    - Parse order_date supporting 3 formats
    - Drop rows with missing customer_id AND order_id
    - Fill missing amounts with median per product
    - Normalize status to controlled vocabulary
    - Create order_year_month column for time-series analysis

    Returns:
        pd.DataFrame: Cleaned order data.
    """
    df = load_csv(RAW_DATA / "orders.csv")

    print("\nOrders BEFORE cleaning:", len(df), "rows")

    # parse date
    df["order_date"] = df["order_date"].apply(parse_date)

    # drop rows where both id null
    df = df.dropna(subset=["customer_id", "order_id"], how="all")

    # fill missing amount with median per product
    df["amount"] = df.groupby("product")["amount"].transform(
        lambda x: x.fillna(x.median())
    )

    # normalize status
    status_map = {
        "done": "completed",
        "canceled": "cancelled"
    }

    df["status"] = df["status"].replace(status_map)
    df["status"] = df["status"].str.lower()

    # order_year_month column
    df["order_year_month"] = df["order_date"].dt.strftime("%Y-%m")

    print("Orders AFTER cleaning:", len(df), "rows")

    df.to_csv(PROCESSED_DATA / "orders_clean.csv", index=False)
    return df


# -------------------------
# Main
# -------------------------

def main():
    """Main entry point for data cleaning pipeline."""
    print("\n" + "="*60)
    print("Starting Data Cleaning Pipeline...")
    print("="*60)

    clean_customers()
    clean_orders()

    print("\n" + "="*60)
    print("Data Cleaning Completed Successfully!")
    print("="*60)


if __name__ == "__main__":
    main()





#                         Yaha hum clean_data.py script use kar rahe hain.

# Ye script:

# 1.duplicate remove karti hai

# 2.emails lowercase karti hai

# 3.invalid email detect karti hai

# 4.date format fix karti hai

# 5.missing values fill karti hai

# Example:

# Before:

# ALI@GMAIL.COM

# After:

# ali@gmail.com

# Clean data save hota hai:

# customers_clean.csv
# orders_clean.csv