import io

import pandas as pd


def convert_dataframe_to_csv(df):
    """
    Convert DataFrame into downloadable CSV bytes.
    """
    return df.to_csv(index=False).encode("utf-8")


def convert_dataframe_to_excel(df):
    """
    Convert DataFrame into downloadable Excel bytes.
    """
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sales Report")

    return output.getvalue()
