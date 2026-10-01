import pandas as pd
import numpy as np

def clean_sales_data(df):
    """
    Clean and prepare sales data for analysis.
    """
    cleaned_df = df.copy()

    # Remove duplicate rows
    cleaned_df = cleaned_df.drop_duplicates()

    # Convert date column
    if "Order_Date" in cleaned_df.columns:
        cleaned_df["Order_Date"] = pd.to_datetime(
            cleaned_df["Order_Date"],
            errors="coerce"
        )

    # Convert numeric columns
    numeric_columns = [
        "Quantity",
        "Unit_Price",
        "Discount",
        "Sales",
        "Profit"
    ]

    for column in numeric_columns:
        if column in cleaned_df.columns:
            cleaned_df[column] = pd.to_numeric(
                cleaned_df[column],
                errors="coerce"
            )

    # Fill missing quantity and price values
    if "Quantity" in cleaned_df.columns:
        cleaned_df["Quantity"] = cleaned_df["Quantity"].fillna(0)

    if "Unit_Price" in cleaned_df.columns:
        cleaned_df["Unit_Price"] = cleaned_df["Unit_Price"].fillna(0)

    # Create default discount column
    if "Discount" not in cleaned_df.columns:
        cleaned_df["Discount"] = 0

    cleaned_df["Discount"] = cleaned_df["Discount"].fillna(0)

    # Calculate sales if missing
    if "Sales" not in cleaned_df.columns:
        cleaned_df["Sales"] = (
            cleaned_df["Quantity"]
            * cleaned_df["Unit_Price"]
            * (1 - cleaned_df["Discount"])
        )

    # Calculate profit if missing
    if "Profit" not in cleaned_df.columns:
        cleaned_df["Profit"] = 0

    # Remove invalid rows
    cleaned_df = cleaned_df[
        cleaned_df["Quantity"] >= 0
    ]

    cleaned_df = cleaned_df[
        cleaned_df["Unit_Price"] >= 0
    ]

    # Add time-based columns
    if "Order_Date" in cleaned_df.columns:
        cleaned_df["Year"] = cleaned_df["Order_Date"].dt.year
        cleaned_df["Month"] = cleaned_df["Order_Date"].dt.month
        cleaned_df["Month_Name"] = cleaned_df["Order_Date"].dt.month_name()
        cleaned_df["Quarter"] = (
            cleaned_df["Order_Date"].dt.to_period("Q").astype(str)
        )

    return cleaned_df.reset_index(drop=True)


def get_data_quality_report(df):
    """
    Generate a data quality report.
    """
    report = pd.DataFrame({
        "Column": df.columns,
        "Data_Type": df.dtypes.astype(str).values,
        "Missing_Values": df.isnull().sum().values,
        "Unique_Values": df.nunique().values
    })

    return report
