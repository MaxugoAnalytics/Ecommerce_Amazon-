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

.visual-box {
    background-color: #393939;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
    margin: 10px;
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

# Top Key Metrics
st.header("Key Metrics")
metrics = st.columns(5)
metrics[0].metric("Total Revenue", f"${amazon['Order'].sum():,.2f}")
metrics[1].metric("Total Orders", f"{amazon['Order'].sum():,.0f}")
metrics[2].metric("Unique Products", f"{amazon['Style'].nunique():,.0f}")
metrics[3].metric("States Covered", f"{amazon['ship-state'].nunique():,.0f}")
metrics[4].metric("Fulfillment Types", f"{amazon['Fulfilment'].nunique():,.0f}")

# Data Visualizations
# Row 1
row1 = st.columns(3)
with row1[0]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Orders by Fulfilment Type</div>', unsafe_allow_html=True)
    
    # Dropdown filter with "All" option
    fulfilment_types = st.selectbox("Select Fulfilment Type:", options=["All"] + list(amazon["Fulfilment"].unique()), key="fulfilment_filter")
    filtered_data = amazon if fulfilment_types == "All" else amazon[amazon["Fulfilment"] == fulfilment_types]
    
    fulfilment_data = filtered_data.groupby("Fulfilment")["Order"].sum().reset_index()
    fig_fulfilment = px.pie(
        fulfilment_data,
        names="Fulfilment",
        values="Order",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_fulfilment, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row1[1]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Revenue by Product Style</div>', unsafe_allow_html=True)
    
    # Dropdown filter with "All" option
    product_styles = st.selectbox("Select Product Style:", options=["All"] + list(amazon["Style"].unique()), key="style_filter")
    filtered_data = amazon if product_styles == "All" else amazon[amazon["Style"] == product_styles]
    
    style_data = filtered_data.groupby("Style")["Order"].sum().reset_index()
    fig_style = px.bar(
        style_data,
        x="Style",
        y="Order",
        color="Style",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_style, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row1[2]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Orders by Day</div>', unsafe_allow_html=True)
    
    # Dropdown filter with "All" option
    days = st.selectbox("Select Day:", options=["All"] + list(amazon["Day"].unique()), key="day_filter")
    filtered_data = amazon if days == "All" else amazon[amazon["Day"] == days]
    
    daily_orders = filtered_data.groupby("Day")["Order"].sum().reset_index()
    fig_day = px.line(
        daily_orders,
        x="Day",
        y="Order",
        labels={"Day": "Day", "Order": "Orders"}
    )
    st.plotly_chart(fig_day, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Row 2
row2 = st.columns(2)
with row2[0]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Average Revenue by State</div>', unsafe_allow_html=True)
    
    # Dropdown filter with "All" option
    states = st.selectbox("Select Shipping State:", options=["All"] + list(amazon["ship-state"].unique()), key="state_filter")
    filtered_data = amazon if states == "All" else amazon[amazon["ship-state"] == states]
    
    state_avg_revenue = filtered_data.groupby("ship-state")["Order"].mean().reset_index()
    fig_avg_state = px.bar(
        state_avg_revenue,
        x="ship-state",
        y="Order",
        color="ship-state",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_avg_state, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row2[1]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">B2B vs Consumer Orders</div>', unsafe_allow_html=True)
    
    # Dropdown filter with "All" option
    b2b_types = st.selectbox("Select Business Type:", options=["All"] + list(amazon["B2B"].unique()), key="b2b_filter")
    filtered_data = amazon if b2b_types == "All" else amazon[amazon["B2B"] == b2b_types]
    
    b2b_data = filtered_data.groupby("B2B")["Order"].sum().reset_index()
    fig_b2b = px.pie(
        b2b_data,
        names="B2B",
        values="Order",
        color_discrete_sequence=["#1f77b4", "#ff7f0e"]
    )
    st.plotly_chart(fig_b2b, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)





