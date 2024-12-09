import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Amazon Sales Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load and cache data
@st.cache_data
def load_data():
    url = 'https://drive.google.com/uc?id=1j-6nn-SvsVlw_ySdMa73dbmaa92ehq-Z'
    amazon = pd.read_csv(url)
    return amazon

# Load data
amazon = load_data()

col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
        width=100
    )
with col_title:
    st.title("Amazon Sales Report Dashboard by Maxwell Adigwe")

# Sidebar filters
st.sidebar.header("Filters")
selected_styles = st.sidebar.multiselect(
    "Select Product Styles",
    options=amazon["Style"].unique(),
    default=amazon["Style"].unique()
)
selected_states = st.sidebar.multiselect(
    "Select Shipping States",
    options=amazon["ship-state"].unique(),
    default=amazon["ship-state"].unique()
)
selected_fulfilment = st.sidebar.multiselect(
    "Select Fulfilment Type",
    options=amazon["Fulfilment"].unique(),
    default=amazon["Fulfilment"].unique()
)
selected_b2b = st.sidebar.multiselect(
    "Business Type",
    options=amazon["B2B"].unique(),
    default=amazon["B2B"].unique()
)

# Apply filters
filtered_data = amazon[(
    amazon["Style"].isin(selected_styles)) &
    (amazon["ship-state"].isin(selected_states)) &
    (amazon["Fulfilment"].isin(selected_fulfilment)) &
    (amazon["B2B"].isin(selected_b2b))
]

# Add calculated columns
filtered_data["Revenue per Order"] = filtered_data["Order"]  # Assuming 'Order' is revenue in this dataset
filtered_data["Is Weekend"] = filtered_data["Day"].isin(["Saturday", "Sunday"])
filtered_data["Has Promotion"] = filtered_data["promotion-ids"] != "No Promotion"

# Layout: Top Metrics
st.header("Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Total Revenue", f"${filtered_data['Revenue per Order'].sum():,.2f}")
with col2:
    st.metric("Total Orders", f"{filtered_data['Order'].sum():,.0f}")
with col3:
    st.metric("Unique Products", f"{filtered_data['Style'].nunique():,.0f}")
with col4:
    st.metric("States Covered", f"{filtered_data['ship-state'].nunique():,.0f}")
with col5:
    st.metric("Promotion Usage (%)", f"{(filtered_data['Has Promotion'].mean() * 100):.2f}%")

# Organizing visuals into two rows with four columns each
col1, col2, col3, col4 = st.columns(4)

# First row of visuals
with col1:
    # Fulfilment breakdown (Pie Chart)
    st.subheader("Orders by Fulfilment Type")
    fulfilment_data = filtered_data.groupby("Fulfilment")["Order"].sum().reset_index()
    fig_fulfilment = px.pie(
        fulfilment_data,
        names="Fulfilment",
        values="Order",
        color_discrete_sequence=px.colors.qualitative.Set3,
        title="Orders by Fulfilment Type"
    )
    st.plotly_chart(fig_fulfilment, use_container_width=True)

with col2:
    # Orders by Day (Line Chart)
    st.subheader("Daily Orders Trend")
    daily_orders = filtered_data.groupby("Day")["Order"].sum().reset_index()
    fig_day = px.line(
        daily_orders,
        x="Day",
        y="Order",
        title="Orders by Day",
        labels={"Day": "Day", "Order": "Total Orders"}
    )
    st.plotly_chart(fig_day, use_container_width=True)

with col3:
    # Orders by state (Bar Chart)
    st.subheader("Orders by Shipping State")
    st.write("This bar chart shows the distribution of orders across different shipping states.")
    state_data = filtered_data.groupby("ship-state")["Order"].sum().reset_index()
    fig_state = px.bar(
        state_data,
        x="ship-state",
        y="Order",
        title="Orders by State",
        labels={"ship-state": "State", "Order": "Total Orders"},
        color="ship-state",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_state, use_container_width=True)

with col4:
    # B2B vs. Non-B2B Orders (Pie Chart)
    st.subheader("B2B vs. Consumer Orders")
    b2b_data = filtered_data.groupby("B2B")["Order"].sum().reset_index()
    fig_b2b = px.pie(
        b2b_data,
        names="B2B",
        values="Order",
        title="B2B Orders vs. Consumer Orders",
        color_discrete_sequence=["#1f77b4", "#ff7f0e"]
    )
    st.plotly_chart(fig_b2b, use_container_width=True)

# Second row of visuals
col5, col6, col7, col8 = st.columns(4)

with col5:
    # Weekly Revenue Trends (Line Chart)
    st.subheader("Weekly Revenue Trends")
    weekly_revenue = filtered_data.groupby("Week")["Revenue per Order"].sum().reset_index()
    fig_weekly_revenue = px.line(
        weekly_revenue,
        x="Week",
        y="Revenue per Order",
        title="Weekly Revenue Trends",
        labels={"Week": "Week Number", "Revenue per Order": "Revenue"}
    )
    st.plotly_chart(fig_weekly_revenue, use_container_width=True)

with col6:
    # Revenue Distribution (Histogram)
    st.subheader("Revenue Distribution")
    fig_hist = px.histogram(
        filtered_data,
        x="Revenue per Order",
        title="Distribution of Revenue per Order",
        color_discrete_sequence=["#636EFA"]
    )
    st.plotly_chart(fig_hist, use_container_width=True)


st.subheader("Monthly Orders Trend")
monthly_orders = filtered_data.groupby("Month")["Order"].sum().reset_index()
fig_month = px.line(
    monthly_orders,
    x="Month",
    y="Order",
    title="Monthly Orders Trend",
    labels={"Month": "Month", "Order": "Total Orders"}
)
st.plotly_chart(fig_month, use_container_width=True)


with col8:
    # Revenue vs Orders Scatter Plot
    st.subheader("Revenue vs Orders")
    fig_revenue_orders = px.scatter(
        filtered_data,
        x="Order",
        y="Revenue per Order",
        color="Style",
        title="Revenue vs Orders",
        labels={"Order": "Total Orders", "Revenue per Order": "Revenue per Order"}
    )
    st.plotly_chart(fig_revenue_orders, use_container_width=True)

