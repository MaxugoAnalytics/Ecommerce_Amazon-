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

# Function to handle "Select All" logic
def apply_filter(options, selected):
    if "All" in selected:
        return options[1:]  # Exclude "All" when filtering
    return selected

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

# Second Row: Visualizations with filters
col3, col4, col5, col6, col7 = st.columns(5)

with col3:
    # Sales by Method
    st.subheader("Sales by Method")
    method_options = ["All"] + df_cleaned["SalesMethod"].unique().tolist()
    method_filter = st.multiselect("Filter by Sales Method", options=method_options, default="All")
    filtered_method = df_cleaned[df_cleaned["SalesMethod"].isin(apply_filter(method_options, method_filter))]
    sales_method = filtered_method.groupby("SalesMethod")["TotalSales"].sum().reset_index()
    st.bar_chart(sales_method.set_index("SalesMethod"))

with col4:
    # Yearly Sales vs Profit Comparison
    st.subheader("Yearly Sales vs Profit")
    year_options = ["All"] + df_cleaned["Year"].unique().tolist()
    year_filter = st.multiselect("Filter by Year", options=year_options, default="All")
    filtered_year = df_cleaned[df_cleaned["Year"].isin(apply_filter(year_options, year_filter))]
    yearly_comparison = filtered_year.groupby("Year")[["TotalSales", "OperatingProfit"]].sum().reset_index()
    st.bar_chart(yearly_comparison.set_index("Year"))

with col5:
    # Profit Margin Trends
    st.subheader("Yearly Profit Margin Trends")
    product_options = ["All"] + df_cleaned["Product"].unique().tolist()
    product_filter = st.multiselect("Filter by Product", options=product_options, default="All")
    filtered_product = df_cleaned[df_cleaned["Product"].isin(apply_filter(product_options, product_filter))]
    filtered_product["ProfitMargin"] = (
        filtered_product["OperatingProfit"] / filtered_product["TotalSales"]
    ) * 100
    yearly_profit_margin = filtered_product.groupby("Year")["ProfitMargin"].mean().reset_index()
    st.line_chart(yearly_profit_margin.set_index("Year"), use_container_width=True)

with col6:
    # Regional Sales Distribution
    st.subheader("Regional Sales Distribution")
    region_options = ["All"] + df_cleaned["Region"].unique().tolist()
    region_filter = st.multiselect("Filter by Region", options=region_options, default="All")
    filtered_region = df_cleaned[df_cleaned["Region"].isin(apply_filter(region_options, region_filter))]
    regional_sales = filtered_region.groupby("Region")["TotalSales"].sum().reset_index()
    st.bar_chart(regional_sales.set_index("Region"))

with col7:
    # Top Selling Products
    st.subheader("Top 5 Selling Products")
    state_options = ["All"] + df_cleaned["State"].unique().tolist()
    state_filter = st.multiselect("Filter by State", options=state_options, default="All")
    filtered_state = df_cleaned[df_cleaned["State"].isin(apply_filter(state_options, state_filter))]
    top_products = filtered_state.groupby("Product")["TotalSales"].sum().nlargest(5).reset_index()
    st.bar_chart(top_products.set_index("Product"))

# Third Row: Additional Visualizations with Filters
col8, col9, col10, col11, col12 = st.columns(5)

with col8:
    # Sales vs Operating Profit Scatter Plot
    st.subheader("Sales vs Operating Profit")
    city_options = ["All"] + df_cleaned["City"].unique().tolist()
    city_filter = st.multiselect("Filter by City", options=city_options, default="All")
    filtered_city = df_cleaned[df_cleaned["City"].isin(apply_filter(city_options, city_filter))]
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
