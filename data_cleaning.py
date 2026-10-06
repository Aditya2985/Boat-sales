"""
============================================================
 boAt Sales Analytics - Data Cleaning & Preparation
============================================================
 Cleans the raw CSV, validates data quality, creates
 Power BI-ready export with proper formatting.
============================================================
"""

import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")

INPUT_CSV = os.path.join(os.path.dirname(__file__), "boat_sales_data.csv")
OUTPUT_CSV = os.path.join(os.path.dirname(__file__), "boat_sales_cleaned.csv")


def load_data():
    """Load raw CSV data."""
    df = pd.read_csv(INPUT_CSV)
    print(f"  [LOAD] Raw dataset: {df.shape[0]:,} rows x {df.shape[1]} columns")
    return df


def data_quality_check(df):
    """Run data quality checks and print report."""
    print(f"\n{'='*60}")
    print("  DATA QUALITY REPORT")
    print(f"{'='*60}")

    # Null check
    nulls = df.isnull().sum()
    null_cols = nulls[nulls > 0]
    if len(null_cols) == 0:
        print("  [OK] No null values found")
    else:
        print("  [WARNING] Null values found:")
        for col, count in null_cols.items():
            print(f"    - {col}: {count} nulls")

    # Duplicate check
    dupes = df.duplicated(subset=["Order_ID"]).sum()
    print(f"  [OK] Duplicate Order IDs: {dupes}")

    # Data type check
    print(f"\n  Column Data Types:")
    for col in df.columns:
        print(f"    {col:<20s} : {df[col].dtype}")

    # Value range checks
    print(f"\n  Value Range Checks:")
    print(f"    Revenue range    : {df['Revenue'].min():,.0f} - {df['Revenue'].max():,.0f}")
    print(f"    Profit range     : {df['Profit'].min():,.0f} - {df['Profit'].max():,.0f}")
    print(f"    Rating range     : {df['Rating'].min()} - {df['Rating'].max()}")
    print(f"    Quantity range   : {df['Quantity'].min()} - {df['Quantity'].max()}")
    print(f"    Discount range   : {df['Discount_Pct'].min()}% - {df['Discount_Pct'].max()}%")
    print(f"    Unit Price range : {df['Unit_Price'].min():,} - {df['Unit_Price'].max():,}")

    # Unique value counts
    print(f"\n  Unique Value Counts:")
    for col in ["State", "City", "Category", "Product_Name", "Sales_Channel",
                "Payment_Mode", "Age_Group", "Gender", "Month", "Region"]:
        print(f"    {col:<20s} : {df[col].nunique()} unique values")

    return df


def clean_data(df):
    """Clean and prepare data for Power BI."""
    print(f"\n{'='*60}")
    print("  DATA CLEANING STEPS")
    print(f"{'='*60}")

    # 1. Parse dates properly
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], format="%d-%m-%Y", errors="coerce")
    print("  [1] Parsed Order_Date to datetime")

    # 2. Ensure no negative revenues (data integrity)
    neg_rev = (df["Revenue"] < 0).sum()
    if neg_rev > 0:
        df = df[df["Revenue"] >= 0]
        print(f"  [2] Removed {neg_rev} rows with negative revenue")
    else:
        print("  [2] No negative revenues found - OK")

    # 3. Cap ratings to valid range [1.0, 5.0]
    df["Rating"] = df["Rating"].clip(1.0, 5.0)
    print("  [3] Ratings clipped to [1.0, 5.0] range")

    # 4. Create additional calculated columns for Power BI
    df["Profit_Margin"] = round((df["Profit"] / df["Revenue"]) * 100, 1)
    print("  [4] Added Profit_Margin column")

    # 5. Create Quarter column
    df["Quarter"] = df["Order_Date"].dt.quarter
    df["Quarter_Label"] = "Q" + df["Quarter"].astype(str)
    print("  [5] Added Quarter and Quarter_Label columns")

    # 6. Create Day of Week
    df["Day_of_Week"] = df["Order_Date"].dt.day_name()
    print("  [6] Added Day_of_Week column")

    # 7. Create Price Segment
    df["Price_Segment"] = pd.cut(
        df["Unit_Price"],
        bins=[0, 500, 1000, 2000, 3000, 5000],
        labels=["Budget (<500)", "Value (500-1K)", "Mid (1K-2K)", "Premium (2K-3K)", "Ultra (3K+)"]
    )
    print("  [7] Added Price_Segment column")

    # 8. Format date back for CSV export (DD-MM-YYYY for Power BI)
    df["Order_Date"] = df["Order_Date"].dt.strftime("%d-%m-%Y")
    print("  [8] Formatted Order_Date as DD-MM-YYYY")

    # 9. Sort by Order_ID
    df = df.sort_values("Order_ID").reset_index(drop=True)
    print("  [9] Sorted by Order_ID")

    return df


def generate_summary_stats(df):
    """Generate summary for verification against Power BI."""
    print(f"\n{'='*60}")
    print("  FINAL DATASET SUMMARY (verify in Power BI)")
    print(f"{'='*60}")
    print(f"  Total Records      : {len(df):,}")
    print(f"  Total Revenue      : Rs.{df['Revenue'].sum():,.0f}")
    print(f"  Total Profit       : Rs.{df['Profit'].sum():,.0f}")
    print(f"  Total Orders       : {len(df):,}")
    print(f"  Avg Rating         : {df['Rating'].mean():.2f}")
    print(f"  Avg Quantity       : {df['Quantity'].mean():.2f}")

    print(f"\n  Category-wise Orders:")
    for cat, count in df["Category"].value_counts().items():
        print(f"    {cat:<20s} : {count:,}")

    print(f"\n  Channel-wise Revenue:")
    for ch, rev in df.groupby("Sales_Channel")["Revenue"].sum().sort_values(ascending=False).items():
        print(f"    {ch:<20s} : Rs.{rev:,.0f}")

    print(f"\n  Columns in cleaned dataset ({len(df.columns)}):")
    for col in df.columns:
        print(f"    - {col}")


def export_cleaned(df):
    """Export cleaned dataset."""
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
    file_size = os.path.getsize(OUTPUT_CSV)
    print(f"\n  [OK] Cleaned dataset exported: {OUTPUT_CSV}")
    print(f"       File size: {file_size / 1024:.1f} KB")
    print(f"       Rows: {len(df):,} | Columns: {len(df.columns)}")


# ─────────────────── MAIN ───────────────────

if __name__ == "__main__":
    print("\n  boAt Sales Analytics - Data Cleaning Pipeline")
    print("  " + "-"*50)

    df = load_data()
    df = data_quality_check(df)
    df = clean_data(df)
    generate_summary_stats(df)
    export_cleaned(df)

    print(f"\n  [DONE] Data is ready for Power BI import!\n")
