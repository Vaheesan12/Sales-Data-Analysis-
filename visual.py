import plotly.express as px
import plotly.graph_objects as go


def category_sales_chart(category_data):
    figure = px.bar(
        category_data,
        x="Category",
        y="Sales",
        color="Category",
        title="Sales by Category",
        text_auto=".2s"
    )

    figure.update_layout(
        xaxis_title="Category",
        yaxis_title="Sales",
        showlegend=False
    )

    return figure


def regional_sales_chart(region_data):
    figure = px.pie(
        region_data,
        names="Region",
        values="Sales",
        title="Sales Distribution by Region"
    )

    return figure


def monthly_sales_chart(monthly_data):
    figure = px.line(
        monthly_data,
        x="Month_Name",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    figure.update_layout(
        xaxis_title="Month",
        yaxis_title="Sales"
    )

    return figure


def profit_sales_chart(df):
    figure = px.scatter(
        df,
        x="Sales",
        y="Profit",
        color="Category",
        hover_data=["Product", "Region"],
        title="Sales and Profit Relationship"
    )

    return figure


def top_products_chart(product_data):
    figure = px.bar(
        product_data.sort_values("Sales"),
        x="Sales",
        y="Product",
        orientation="h",
        color="Profit",
        title="Top-Selling Products",
        text_auto=".2s"
    )

    return figure
