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
.dashboard-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 15px;
}

.visual-box, [data-testid="stMetric"] {
    background-color: #393939;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
    margin: 0;
    text-align: center;
}

.visual-title {
    font-size: 16px;
    font-weight: bold;
    color: #f5f5f5;
    margin-bottom: 10px;
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

# Centered Title
st.markdown("<h1 style='text-align: center; color: #232F3E;'>Amazon Sales Dashboard</h1>", unsafe_allow_html=True)

# Dashboard Metrics (Row 1)
st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)
st.metric("Total Revenue", f"${amazon['Order'].sum():,.2f}")
st.metric("Total Orders", f"{amazon['Order'].sum():,.0f}")
st.metric("Unique Products", f"{amazon['Style'].nunique():,.0f}")
st.metric("States Covered", f"{amazon['ship-state'].nunique():,.0f}")
st.metric("Fulfillment Types", f"{amazon['Fulfilment'].nunique():,.0f}")
st.markdown('</div>', unsafe_allow_html=True)

# Visualizations (Rows 2 and 3)
st.markdown('<div class="dashboard-container">', unsafe_allow_html=True)

# Visualization 1: Orders by Fulfilment Type
with st.container():
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Orders by Fulfilment Type</div>', unsafe_allow_html=True)
    fulfilment_types = st.selectbox("Select Fulfilment Type:", ["All"] + list(amazon["Fulfilment"].unique()), key="fulfilment_filter")
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

# Visualization 2: Revenue by Product Style
with st.container():
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Revenue by Product Style</div>', unsafe_allow_html=True)
    product_styles = st.selectbox("Select Product Style:", ["All"] + list(amazon["Style"].unique()), key="style_filter")
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

# Visualization 3: Orders by Day
with st.container():
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Orders by Day</div>', unsafe_allow_html=True)
    days = st.selectbox("Select Day:", ["All"] + list(amazon["Day"].unique()), key="day_filter")
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

# Visualization 4: Average Revenue by State
with st.container():
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Average Revenue by State</div>', unsafe_allow_html=True)
    states = st.selectbox("Select Shipping State:", ["All"] + list(amazon["ship-state"].unique()), key="state_filter")
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

# Visualization 5: B2B vs Consumer Orders
with st.container():
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">B2B vs Consumer Orders</div>', unsafe_allow_html=True)
    b2b_types = st.selectbox("Select Business Type:", ["All"] + list(amazon["B2B"].unique()), key="b2b_filter")
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

st.markdown('</div>', unsafe_allow_html=True)






