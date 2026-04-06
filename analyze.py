"""Data Analysis and Aggregation Module.

This module performs merging of multiple datasets and derives business insights
through various aggregations and transformations.
"""

import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
RAW_DATA = BASE_DIR / "data" / "raw"
PROCESSED_DATA = BASE_DIR / "data" / "processed"


def load_csv(file_path: str) -> pd.DataFrame:
    """Load CSV file with error handling.
    
    Args:
        file_path: Path to CSV file.
        
    Returns:
        pd.DataFrame: Loaded data.
        
    Raises:
        FileNotFoundError: If file doesn't exist.
    """
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        raise


# -----------------------
# Load Cleaned Data
# -----------------------

def main():
    """Main analysis pipeline: merge data and generate insights."""
    
    print("\n" + "="*60)
    print("Starting Data Analysis Pipeline...")
    print("="*60)

    # Load cleaned data
    print("\nLoading cleaned datasets...")
    customers = load_csv(PROCESSED_DATA / "customers_clean.csv")
    orders = load_csv(PROCESSED_DATA / "orders_clean.csv")
    products = load_csv(RAW_DATA / "products.csv")

    # -----------------------
    # Merge Data
    # -----------------------

    print("\nMerging datasets...")
    orders_with_customers = pd.merge(
        orders,
        customers,
        on="customer_id",
        how="left"
    )

    full_data = pd.merge(
        orders_with_customers,
        products,
        left_on="product",
        right_on="product_name",
        how="left"
    )

    print(f"  Total merged rows: {len(full_data)}")
    
    # Validate merge quality
    no_customer = orders[~orders["customer_id"].isin(customers["customer_id"])].shape[0]
    no_product = full_data[full_data["category"].isnull()].shape[0]
    print(f"  Unmatched: {no_customer} orders with no customer, {no_product} with no product")


    # -----------------------
    # 1. Monthly Revenue
    # -----------------------

    print("\n1. Computing monthly revenue...")
    monthly_revenue = full_data[full_data["status"] == "completed"]
    monthly_revenue = monthly_revenue.groupby("order_year_month")["amount"].sum().reset_index()
    monthly_revenue.to_csv(PROCESSED_DATA / "monthly_revenue.csv", index=False)
    print(f"   Generated {len(monthly_revenue)} months of revenue data")


    # -----------------------
    # 2. Top Customers
    # -----------------------

    print("\n2. Identifying top 10 customers...")
    completed_orders = full_data[full_data["status"] == "completed"]

    top_customers = completed_orders.groupby(
        ["customer_id", "name", "region"]
    )["amount"].sum().reset_index()

    top_customers = top_customers.sort_values(
        "amount",
        ascending=False
    ).head(10)

    top_customers.rename(columns={"amount": "total_spend"}, inplace=True)

    # Churn Detection (90 days)
    latest_date = pd.to_datetime(full_data["order_date"]).max()
    last_orders = completed_orders.groupby("customer_id")["order_date"].max().reset_index()
    last_orders["order_date"] = pd.to_datetime(last_orders["order_date"])
    last_orders["churned"] = (latest_date - last_orders["order_date"]).dt.days > 90

    top_customers = pd.merge(
        top_customers,
        last_orders[["customer_id", "churned"]],
        on="customer_id",
        how="left"
    )

    top_customers.to_csv(PROCESSED_DATA / "top_customers.csv", index=False)
    print(f"   Identified {top_customers['churned'].sum()} churned customers")


    # -----------------------
    # 3. Category Performance
    # -----------------------

    print("\n3. Analyzing category performance...")
    category_perf = completed_orders.groupby("category").agg(
        total_revenue=("amount", "sum"),
        avg_order_value=("amount", "mean"),
        number_of_orders=("amount", "count")
    ).reset_index()

    category_perf.to_csv(PROCESSED_DATA / "category_performance.csv", index=False)
    print(f"   Analyzed {len(category_perf)} product categories")


    # -----------------------
    # 4. Regional Analysis
    # -----------------------

    print("\n4. Analyzing regional performance...")
    regional = full_data.groupby("region").agg(
        customers=("customer_id", "nunique"),
        orders=("order_id", "count"),
        revenue=("amount", "sum")
    ).reset_index()

    regional["avg_revenue_per_customer"] = regional["revenue"] / regional["customers"]

    regional.to_csv(PROCESSED_DATA / "regional_analysis.csv", index=False)
    print(f"   Analyzed {len(regional)} regions")

    print("\n" + "="*60)
    print("Analysis Completed Successfully!")
    print("="*60)


if __name__ == "__main__":
    main()