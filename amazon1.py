import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Amazon Sales Dashboard by Maxwell Adigwe",
    layout="wide",
)

# CSS Styling for Metrics
st.markdown("""
<style>
[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
    border-radius: 8px;
}

[data-testid="stMetricLabel"] {
    font-weight: bold;
    font-size: 14px;
    color: #f5f5f5;
}

[data-testid="stMetricValue"] {
    font-size: 24px;
    font-weight: bold;
    color: #1dbf73;
}

[data-testid="stMetricDelta"] {
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# Load and cache data
@st.cache_data
def load_data():
    url = 'https://drive.google.com/uc?id=1j-6nn-SvsVlw_ySdMa73dbmaa92ehq-Z'
    amazon = pd.read_csv(url)
    return amazon

# Load data
amazon = load_data()

# Centered Title with Styling
st.markdown(""" 
    <style>
        .centered-title {
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            margin-top: -50px;  /* Adjust if necessary */
            color: #232F3E;
        }
    </style>
    <div class="centered-title">Amazon Sales Dashboard</div>
""", unsafe_allow_html=True)

# Sidebar filters (Multi-select options)
st.sidebar.header("Filters")
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
    "Select Business Type",
    options=amazon["B2B"].unique(),
    default=amazon["B2B"].unique()
)
selected_days = st.sidebar.multiselect(
    "Select Days",
    options=amazon["Day"].unique(),
    default=amazon["Day"].unique()
)

# Apply filters
filtered_data = amazon[
    (amazon["ship-state"].isin(selected_states)) &
    (amazon["Fulfilment"].isin(selected_fulfilment)) &
    (amazon["B2B"].isin(selected_b2b)) &
    (amazon["Day"].isin(selected_days))
]

# Add calculated columns
filtered_data["Revenue per Order"] = filtered_data["Order"]
filtered_data["Is Weekend"] = filtered_data["Day"].isin(["Saturday", "Sunday"])
filtered_data["Has Promotion"] = filtered_data["promotion-ids"] != "No Promotion"

# Top Key Metrics
st.header("Key Metrics")
metrics = st.columns(5)
metrics[0].metric("Total Revenue", f"${filtered_data['Revenue per Order'].sum():,.2f}")
metrics[1].metric("Total Orders", f"{filtered_data['Order'].sum():,.0f}")
metrics[2].metric("Unique Products", f"{filtered_data['Style'].nunique():,.0f}")
metrics[3].metric("States Covered", f"{filtered_data['ship-state'].nunique():,.0f}")
metrics[4].metric("Promotion Usage (%)", f"{(filtered_data['Has Promotion'].mean() * 100):.2f}%")

# Single Row Visualizations
st.header("Data Visualizations")
st.markdown("---")

# Create columns for all visuals
cols = st.columns(5)

# Orders by Fulfilment Type
with cols[0]:
    fulfilment_data = filtered_data.groupby("Fulfilment")["Order"].sum().reset_index()
    fig_fulfilment = px.pie(
        fulfilment_data,
        names="Fulfilment",
        values="Order",
        title="Orders by Fulfilment Type",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_fulfilment, use_container_width=True)

# Revenue by Product Style (no filter applied)
with cols[1]:
    style_data = filtered_data.groupby("Style")["Revenue per Order"].sum().reset_index()
    fig_style = px.bar(
        style_data,
        x="Style",
        y="Revenue per Order",
        title="Revenue by Product Style",
        color="Style",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_style, use_container_width=True)

# Orders by Day
with cols[2]:
    daily_orders = filtered_data.groupby("Day")["Order"].sum().reset_index()
    fig_day = px.line(
        daily_orders,
        x="Day",
        y="Order",
        title="Orders by Day",
        labels={"Day": "Day", "Order": "Orders"}
    )
    st.plotly_chart(fig_day, use_container_width=True)

# Average Revenue by State
with cols[3]:
    state_avg_revenue = filtered_data.groupby("ship-state")["Revenue per Order"].mean().reset_index()
    fig_avg_state = px.bar(
        state_avg_revenue,
        x="ship-state",
        y="Revenue per Order",
        title="Average Revenue by State",
        color="ship-state",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_avg_state, use_container_width=True)

# B2B vs Consumer Orders
with cols[4]:
    b2b_data = filtered_data.groupby("B2B")["Order"].sum().reset_index()
    fig_b2b = px.pie(
        b2b_data,
        names="B2B",
        values="Order",
        title="B2B vs Consumer Orders",
        color_discrete_sequence=["#1f77b4", "#ff7f0e"]
    )
    st.plotly_chart(fig_b2b, use_container_width=True)



