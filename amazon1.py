import pandas as pd
import plotly.express as px
import streamlit as st
import warnings

warnings.filterwarnings('ignore')

st.title("Interactive Retail Dashboard by Maxwell Adigwe")

# Load data
url = "https://raw.githubusercontent.com/AbhisheakSaraswat/PythonStreamlit/main/Adidas.xlsx"
df_cleaned = pd.read_excel(url)

# Preprocess data
df_cleaned['InvoiceDate'] = pd.to_datetime(df_cleaned['InvoiceDate'])
df_cleaned['Year'] = df_cleaned['InvoiceDate'].dt.year
df_cleaned['Month'] = df_cleaned['InvoiceDate'].dt.month
df_cleaned['Day'] = df_cleaned['InvoiceDate'].dt.day
df_cleaned['Time'] = df_cleaned['InvoiceDate'].dt.time

# First Row: Key Metrics Overview
col1, col2 = st.columns(2)

with col1:
    # Total Sales
    total_sales = df_cleaned["TotalSales"].sum()
    st.metric("Total Sales ($)", f"${total_sales:,.2f}")

with col2:
    # Operating Profit
    total_profit = df_cleaned["OperatingProfit"].sum()
    st.metric("Operating Profit ($)", f"${total_profit:,.2f}")

# Second Row: Visualizations with dropdown filters
col3, col4, col5, col6, col7 = st.columns(5)

with col3:
    # Sales by Method
    st.subheader("Sales by Method")
    method_filter = st.multiselect(
        "Filter by Sales Method", 
        options=["All"] + list(df_cleaned["SalesMethod"].unique()),
        default="All",
        key="method_filter"
    )
    filtered_method = df_cleaned if "All" in method_filter else df_cleaned[df_cleaned["SalesMethod"].isin(method_filter)]
    sales_method = filtered_method.groupby("SalesMethod")["TotalSales"].sum().reset_index()
    st.bar_chart(sales_method.set_index("SalesMethod"))

with col4:
    # Yearly Sales vs Profit Comparison
    st.subheader("Yearly Sales vs Profit")
    year_filter = st.multiselect(
        "Filter by Year",
        options=["All"] + list(df_cleaned["Year"].unique()),
        default="All",
        key="year_filter"
    )
    filtered_year = df_cleaned if "All" in year_filter else df_cleaned[df_cleaned["Year"].isin(year_filter)]
    yearly_comparison = filtered_year.groupby("Year")[["TotalSales", "OperatingProfit"]].sum().reset_index()
    st.bar_chart(yearly_comparison.set_index("Year"))

with col5:
    # Profit Margin Trends
    st.subheader("Yearly Profit Margin Trends")
    product_filter = st.multiselect(
        "Filter by Product",
        options=["All"] + list(df_cleaned["Product"].unique()),
        default="All",
        key="product_filter"
    )
    filtered_product = df_cleaned if "All" in product_filter else df_cleaned[df_cleaned["Product"].isin(product_filter)]
    filtered_product["ProfitMargin"] = (
        filtered_product["OperatingProfit"] / filtered_product["TotalSales"]
    ) * 100
    yearly_profit_margin = filtered_product.groupby("Year")["ProfitMargin"].mean().reset_index()
    st.line_chart(yearly_profit_margin.set_index("Year"), use_container_width=True)

with col6:
    # Regional Sales Distribution
    st.subheader("Regional Sales Distribution")
    region_filter = st.multiselect(
        "Filter by Region",
        options=["All"] + list(df_cleaned["Region"].unique()),
        default="All",
        key="region_filter"
    )
    filtered_region = df_cleaned if "All" in region_filter else df_cleaned[df_cleaned["Region"].isin(region_filter)]
    regional_sales = filtered_region.groupby("Region")["TotalSales"].sum().reset_index()
    st.bar_chart(regional_sales.set_index("Region"))

with col7:
    # Top Selling Products
    st.subheader("Top 5 Selling Products")
    state_filter = st.multiselect(
        "Filter by State",
        options=["All"] + list(df_cleaned["State"].unique()),
        default="All",
        key="state_filter"
    )
    filtered_state = df_cleaned if "All" in state_filter else df_cleaned[df_cleaned["State"].isin(state_filter)]
    top_products = filtered_state.groupby("Product")["TotalSales"].sum().nlargest(5).reset_index()
    st.bar_chart(top_products.set_index("Product"))

# Third Row: Additional Visualizations with Dropdown Filters
col8, col9, col10, col11, col12 = st.columns(5)

with col8:
    # Sales vs Operating Profit Scatter Plot
    st.subheader("Sales vs Operating Profit")
    sales_profit_filter = st.multiselect(
        "Filter by City",
        options=["All"] + list(df_cleaned["City"].unique()),
        default="All",
        key="sales_profit_filter"
    )
    filtered_city = df_cleaned if "All" in sales_profit_filter else df_cleaned[df_cleaned["City"].isin(sales_profit_filter)]
    fig_sales_profit = px.scatter(
        filtered_city, 
        x="TotalSales", 
        y="OperatingProfit", 
        color="Product", 
        template="plotly_dark"
    )
    st.plotly_chart(fig_sales_profit)

with col9:
    # Monthly Sales Trends
    st.subheader("Monthly Sales Trends")
    monthly_sales = filtered_city.groupby("Month")["TotalSales"].sum().reset_index()
    st.line_chart(monthly_sales.set_index("Month"), use_container_width=True)

with col10:
    # Profit Margin Distribution
    st.subheader("Profit Margin Distribution")
    st.bar_chart(filtered_city["ProfitMargin"])

with col11:
    # Profit vs Sales by Region (Scatter Plot)
    st.subheader("Profit vs Sales by Region")
    fig_profit_sales_region = px.scatter(
        filtered_city, 
        x="TotalSales", 
        y="OperatingProfit", 
        color="Region", 
        template="plotly_dark"
    )
    st.plotly_chart(fig_profit_sales_region)

with col12:
    # Daily Sales Trends
    st.subheader("Daily Sales Trends")
    daily_sales = filtered_city.groupby("Day")["TotalSales"].sum().reset_index()
    st.line_chart(daily_sales.set_index("Day"), use_container_width=True)



