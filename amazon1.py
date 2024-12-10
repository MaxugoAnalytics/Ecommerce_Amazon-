import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Amazon Sales Dashboard by Maxwell Adigwe",
    layout="wide",
)

# CSS Styling for Metrics and Visuals
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

.visual-box {
    background-color: #393939;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
}

.visual-title {
    font-size: 16px;
    font-weight: bold;
    color: #f5f5f5;
    text-align: center;
    margin-bottom: 10px;
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
filtered_data = amazon[
    (amazon["Style"].isin(selected_styles)) &
    (amazon["ship-state"].isin(selected_states)) &
    (amazon["Fulfilment"].isin(selected_fulfilment)) &
    (amazon["B2B"].isin(selected_b2b))
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

# Add styled containers for visuals
with cols[0]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Orders by Fulfilment Type</div>', unsafe_allow_html=True)
    fulfilment_data = filtered_data.groupby("Fulfilment")["Order"].sum().reset_index()
    fig_fulfilment = px.pie(
        fulfilment_data,
        names="Fulfilment",
        values="Order",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_fulfilment, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with cols[1]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Revenue by Product Style</div>', unsafe_allow_html=True)
    style_data = filtered_data.groupby("Style")["Revenue per Order"].sum().reset_index()
    fig_style = px.bar(
        style_data,
        x="Style",
        y="Revenue per Order",
        color="Style",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_style, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with cols[2]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Orders by Day</div>', unsafe_allow_html=True)
    daily_orders = filtered_data.groupby("Day")["Order"].sum().reset_index()
    fig_day = px.line(
        daily_orders,
        x="Day",
        y="Order",
        labels={"Day": "Day", "Order": "Orders"}
    )
    st.plotly_chart(fig_day, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with cols[3]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Average Revenue by State</div>', unsafe_allow_html=True)
    state_avg_revenue = filtered_data.groupby("ship-state")["Revenue per Order"].mean().reset_index()
    fig_avg_state = px.bar(
        state_avg_revenue,
        x="ship-state",
        y="Revenue per Order",
        color="ship-state",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_avg_state, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with cols[4]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">B2B vs Consumer Orders</div>', unsafe_allow_html=True)
    b2b_data = filtered_data.groupby("B2B")["Order"].sum().reset_index()
    fig_b2b = px.pie(
        b2b_data,
        names="B2B",
        values="Order",
        color_discrete_sequence=["#1f77b4", "#ff7f0e"]
    )
    st.plotly_chart(fig_b2b, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)











