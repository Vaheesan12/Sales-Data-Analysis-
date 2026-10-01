import streamlit as st
import pandas as pd

from src.data_loader import (
    load_uploaded_file,
    check_required_columns
)

from src.data_cleaning import (
    clean_sales_data,
    get_data_quality_report
)

from src.analysis import (
    calculate_kpis,
    sales_by_category,
    sales_by_region,
    sales_by_product,
    monthly_sales,
    top_products,
    loss_making_products
)

from src.visualizations import (
    category_sales_chart,
    regional_sales_chart,
    monthly_sales_chart,
    profit_sales_chart,
    top_products_chart
)

from src.export import (
    convert_dataframe_to_csv,
    convert_dataframe_to_excel
)

# Page configuration
st.set_page_config(
    page_title="Sales Data Analysis",
    page_icon="📊",
    layout="wide"
)

# Application title
st.title("📊 Sales Data Analysis Dashboard")
st.write(
    "Upload a sales dataset to analyze revenue, profit, products, "
    "categories, regions, and monthly trends."
)

# Sidebar
st.sidebar.header("Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel file",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is None:
    st.info("Please upload a CSV or Excel file to continue.")
    st.stop()

# Load uploaded file
try:
    raw_data = load_uploaded_file(uploaded_file)
except Exception as error:
    st.error(f"Unable to load file: {error}")
    st.stop()

# Display raw data
st.subheader("Uploaded Dataset")
st.dataframe(raw_data.head(10), use_container_width=True)

st.write(f"Rows: {raw_data.shape[0]}")
st.write(f"Columns: {raw_data.shape[1]}")

# Validate columns
missing_columns = check_required_columns(raw_data)

if missing_columns:
    st.warning(
        "The following columns are missing: "
        + ", ".join(missing_columns)
    )

st.info(
        "Required columns are: Order_ID, Order_Date, Category, "
        "Product, Region, Quantity, and Unit_Price."
    )

st.stop()

# Clean data
data = clean_sales_data(raw_data)

# Sidebar filters
st.sidebar.header("Filters")

regions = []
if "Region" in data.columns:
    regions = sorted(data["Region"].dropna().unique())

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=regions,
    default=regions
)

if "Region" in data.columns and regions:
    data = data[data["Region"].isin(selected_regions)]

categories = []
if "Category" in data.columns:
    categories = sorted(data["Category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=categories,
    default=categories
)

if "Category" in data.columns and categories:
    data = data[data["Category"].isin(selected_categories)]

# Date filters
if "Order_Date" in data.columns and not data.empty:
    minimum_date = data["Order_Date"].min().date()
    maximum_date = data["Order_Date"].max().date()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(minimum_date, maximum_date),
        min_value=minimum_date,
        max_value=maximum_date
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
        data = data[
            (data["Order_Date"].dt.date >= start_date)
            & (data["Order_Date"].dt.date <= end_date)
        ]

if data.empty:
    st.warning("No records match the selected filters.")
    st.stop()

# KPI calculations
kpis = calculate_kpis(data)

st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"₹{kpis['Total Sales']:,.2f}"
)

col2.metric(
    "Total Profit",
    f"₹{kpis['Total Profit']:,.2f}"
)

col3.metric(
    "Total Orders",
    f"{kpis['Total Orders']:,}"
)

col4.metric(
    "Profit Margin",
    f"{kpis['Profit Margin']:.2f}%"
)

# Charts
st.subheader("Sales Visualizations")

category_data = sales_by_category(data)
region_data = sales_by_region(data)
product_data = sales_by_product(data)
monthly_data = monthly_sales(data)
top_product_data = top_products(data)

row_one_col1, row_one_col2 = st.columns(2)

with row_one_col1:
    st.plotly_chart(
        category_sales_chart(category_data),
        use_container_width=True
    )

with row_one_col2:
    st.plotly_chart(
        regional_sales_chart(region_data),
        use_container_width=True
    )

row_two_col1, row_two_col2 = st.columns(2)

with row_two_col1:
    st.plotly_chart(
        monthly_sales_chart(monthly_data),
        use_container_width=True
    )

with row_two_col2:
    st.plotly_chart(
        top_products_chart(top_product_data),
        use_container_width=True
    )

st.plotly_chart(
    profit_sales_chart(data),
    use_container_width=True
)

# Summary tables
st.subheader("Analysis Tables")

tab1, tab2, tab3, tab4 = st.tabs([
    "Category Analysis",
    "Region Analysis",
    "Product Analysis",
    "Loss-Making Products"
])

with tab1:
    st.dataframe(
        category_data,
        use_container_width=True
    )

with tab2:
    st.dataframe(
        region_data,
        use_container_width=True
    )

with tab3:
    st.dataframe(
        product_data,
        use_container_width=True
    )

with tab4:
    loss_products = loss_making_products(data)

    if loss_products.empty:
        st.success("No loss-making products found.")
    else:
        st.dataframe(
            loss_products,
            use_container_width=True
        )

# Data quality report
st.subheader("Data Quality Report")

quality_report = get_data_quality_report(data)

st.dataframe(
    quality_report,
    use_container_width=True
)

# Download section
st.subheader("Download Processed Data")

csv_file = convert_dataframe_to_csv(data)

st.download_button(
    label="Download CSV Report",
    data=csv_file,
    file_name="processed_sales_report.csv",
    mime="text/csv"
)

excel_file = convert_dataframe_to_excel(data)

st.download_button(
    label="Download Excel Report",
    data=excel_file,
    file_name="processed_sales_report.xlsx",
    mime=(
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    )
)
