import pandas as pd

def calculate_kpis(df):
    """
    Calculate important sales performance indicators.
    """
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_quantity = df["Quantity"].sum()
    total_orders = df["Order_ID"].nunique()

    average_order_value = (
        total_sales / total_orders
        if total_orders > 0
        else 0
    )

    profit_margin = (
        (total_profit / total_sales) * 100
        if total_sales > 0
        else 0
    )

    return {
        "Total Sales": total_sales,
        "Total Profit": total_profit,
        "Total Quantity": total_quantity,
        "Total Orders": total_orders,
        "Average Order Value": average_order_value,
        "Profit Margin": profit_margin
    }


def sales_by_category(df):
    return (
        df.groupby("Category", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum")
        )
        .sort_values("Sales", ascending=False)
    )


def sales_by_region(df):
    return (
        df.groupby("Region", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum")
        )
        .sort_values("Sales", ascending=False)
    )


def sales_by_product(df):
    return (
        df.groupby("Product", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum")
        )
        .sort_values("Sales", ascending=False)
    )


def monthly_sales(df):
    return (
        df.groupby(["Year", "Month", "Month_Name"], as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .sort_values(["Year", "Month"])
    )


def top_products(df, limit=10):
    product_summary = sales_by_product(df)
    return product_summary.head(limit)


def loss_making_products(df):
    product_summary = sales_by_product(df)
    return product_summary[
        product_summary["Profit"] < 0
    ].sort_values("Profit")
