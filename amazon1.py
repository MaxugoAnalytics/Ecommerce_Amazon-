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

# Sidebar filters (Multi-select options with "All" option)
st.sidebar.header("Filters")

# Function to add an "All" option to multiselect
def add_all_option(filter_name, options, default_value):
    # Add the 'All' option to the list
    all_option = ["All"] + list(options)
    selected_values = st.sidebar.multiselect(
        filter_name,
        options=all_option,
        default=default_value
    )
    
    # If 'All' is selected, return all options
    if "All" in selected_values:
        return options
    else:
        return selected_values

# Apply filters
selected_states = add_all_option(
    "Select Shipping States", amazon["ship-state"].unique(), amazon["ship-state"].unique()
)
selected_fulfilment = add_all_option(
    "Select Fulfilment Type", amazon["Fulfilment"].unique(), amazon["Fulfilment"].unique()
)
selected_b2b = add_all_option(
    "Select Business Type", amazon["B2B"].unique(), amazon["B2B"].unique()
)
selected_days = add_all_option(
    "Select Days", amazon["Day"].unique(), amazon["Day"].unique()
)

# Apply filters to the data
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

# Orders by Fulfilment Type with filter
with cols[0]:
    selected_fulfilment_visual = add_all_option(
        "Select Fulfilment Type for Visual", filtered_data["Fulfilment"].unique(), filtered_data["Fulfilment"].unique()
    )
    fulfilment_data = filtered_data[filtered_data["Fulfilment"].isin(selected_fulfilment_visual)].groupby("Fulfilment")["Order"].sum().reset_index()
    fig_fulfilment = px.pie(
        fulfilment_data,
        names="Fulfilment",
        values="Order",
        title="Orders by Fulfilment Type",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_fulfilment, use_container_width=True)

# Revenue by Product Style with filter
with cols[1]:
    selected_style_visual = add_all_option(
        "Select Product Style for Visual", filtered_data["Style"].unique(), filtered_data["Style"].unique()
    )
    style_data = filtered_data[filtered_data["Style"].isin(selected_style_visual)].groupby("Style")["Revenue per Order"].sum().reset_index()
    fig_style = px.bar(
        style_data,
        x="Style",
        y="Revenue per Order",
        title="Revenue by Product Style",
        color="Style",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_style, use_container_width=True)

# Orders by Day with filter
with cols[2]:
    selected_day_visual = add_all_option(
        "Select Days for Visual", filtered_data["Day"].unique(), filtered_data["Day"].unique()
    )
    daily_orders = filtered_data[filtered_data["Day"].isin(selected_day_visual)].groupby("Day")["Order"].sum().reset_index()
    fig_day = px.line(
        daily_orders,
        x="Day",
        y="Order",
        title="Orders by Day",
        labels={"Day": "Day", "Order": "Orders"}
    )
    st.plotly_chart(fig_day, use_container_width=True)

# Average Revenue by State with filter
with cols[3]:
    selected_state_visual = add_all_option(
        "Select Shipping States for Visual", filtered_data["ship-state"].unique(), filtered_data["ship-state"].unique()
    )
    state_avg_revenue = filtered_data[filtered_data["ship-state"].isin(selected_state_visual)].groupby("ship-state")["Revenue per Order"].mean().reset_index()
    fig_avg_state = px.bar(
        state_avg_revenue,
        x="ship-state",
        y="Revenue per Order",
        title="Average Revenue by State",
        color="ship-state",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_avg_state, use_container_width=True)

# B2B vs Consumer Orders with filter
with cols[4]:
    selected_b2b_visual = add_all_option(
        "Select Business Type for Visual", filtered_data["B2B"].unique(), filtered_data["B2B"].unique()
    )
    b2b_data = filtered_data[filtered_data["B2B"].isin(selected_b2b_visual)].groupby("B2B")["Order"].sum().reset_index()
    fig_b2b = px.pie(
        b2b_data,
        names="B2B",
        values="Order",
        title="B2B vs Consumer Orders",
        color_discrete_sequence=["#1f77b4", "#ff7f0e"]
    )
    st.plotly_chart(fig_b2b, use_container_width=True)





