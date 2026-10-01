import pandas as pd

REQUIRED_COLUMNS = [
    "Order_ID",
    "Order_Date",
    "Category",
    "Product",
    "Region",
    "Quantity",
    "Unit_Price"
]

def load_uploaded_file(uploaded_file):
    """
    Load CSV or Excel file into a Pandas DataFrame.
    """
    if uploaded_file is None:
        return None

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):
        return pd.read_csv(uploaded_file)

    if file_name.endswith(".xlsx") or file_name.endswith(".xls"):
        return pd.read_excel(uploaded_file)

    raise ValueError("Unsupported file format. Upload CSV or Excel file.")


def check_required_columns(df):
    """
    Check whether required columns exist.
    """
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    return missing_columns
