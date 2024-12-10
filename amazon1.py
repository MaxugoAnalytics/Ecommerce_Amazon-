import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Amazon Sales Dashboard by Maxwell Adigwe",
    layout="wide",
)

# CSS for Power BI Styling
st.markdown("""
    <style>
        body {
            background-color: #f4f4f4;
        }

        .main-header {
            background-color: #232F3E;
            color: white;
            text-align: center;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 8px;
        }

        .metric-box, .visual-box {
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        .metric-box .metric-title {
            font-weight: bold;
            color: #555;
        }

        .metric-box .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #232F3E;
        }

        .visual-title {
            font-weight: bold;
            font-size: 16px;
            text-align: center;
            color: #232F3E;
            margin-bottom: 10px;
        }

        .dropdown-label {
            font-weight: bold;
            color: #232F3E;
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

# Header
st.markdown('<div class="main-header">Amazon Sales Dashboard</div>', unsafe_allow_html=True)

# Metrics Section
st.subheader("Key Metrics")
metrics_row = st.columns(5)
metrics_row[0].markdown(
    '<div class="metric-box">'
    '<div class="metric-title">Total Revenue</div>'
    f'<div class="metric-value">${amazon["Order"].sum():,.2f}</div>'
    '</div>',
    unsafe_allow_html=True
)
metrics_row[1].markdown(
    '<div class="metric-box">'
    '<div class="metric-title">Total Orders</div>'
    f'<div class="metric-value">{amazon["Order"].sum():,.0f}</div>'
    '</div>',
    unsafe_allow_html=True
)
metrics_row[2].markdown(
    '<div class="metric-box">'
    '<div class="metric-title">Unique Products</div>'
    f'<div class="metric-value">{amazon["Style"].nunique():,.0f}</div>'
    '</div>',
    unsafe_allow_html=True
)
metrics_row[3].markdown(
    '<div class="metric-box">'
    '<div class="metric-title">States Covered</div>'
    f'<div class="metric-value">{amazon["ship-state"].nunique():,.0f}</div>'
    '</div>',
    unsafe_allow_html=True
)
metrics_row[4].markdown(
    '<div class="metric-box">'
    '<div class="metric-title">Fulfillment Types</div>'
    f'<div class="metric-value">{amazon["Fulfilment"].nunique():,.0f}</div>'
    '</div>',
    unsafe_allow_html=True
)

# Data Visualizations Section
st.subheader("Data Visualizations")

# Row 1
row1 = st.columns(2)

with row1[0]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Orders by Fulfilment Type</div>', unsafe_allow_html=True)

    fulfilment_filter = st.multiselect(
        "Select Fulfilment Type",
        options=list(amazon["Fulfilment"].unique()),
        default=list(amazon["Fulfilment"].unique()),
        key="fulfilment_filter",
    )
    filtered_data = amazon[amazon["Fulfilment"].isin(fulfilment_filter)]

    fulfilment_data = filtered_data.groupby("Fulfilment")["Order"].sum().reset_index()
    fig_fulfilment = px.pie(
        fulfilment_data,
        names="Fulfilment",
        values="Order",
        color_discrete_sequence=px.colors.qualitative.Set3,
        title=""
    )
    st.plotly_chart(fig_fulfilment, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row1[1]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Orders by Day</div>', unsafe_allow_html=True)

    day_filter = st.multiselect(
        "Select Day",
        options=list(amazon["Day"].unique()),
        default=list(amazon["Day"].unique()),
        key="day_filter",
    )
    filtered_data = amazon[amazon["Day"].isin(day_filter)]

    daily_orders = filtered_data.groupby("Day")["Order"].sum().reset_index()
    fig_day = px.line(
        daily_orders,
        x="Day",
        y="Order",
    )
    st.plotly_chart(fig_day, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Row 2
row2 = st.columns(2)

with row2[0]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Average Revenue by State</div>', unsafe_allow_html=True)

    state_filter = st.selectbox(
        "Select Shipping State",
        options=["All"] + list(amazon["ship-state"].unique()),
        key="state_filter",
    )
    filtered_data = amazon if state_filter == "All" else amazon[amazon["ship-state"] == state_filter]

    state_avg_revenue = filtered_data.groupby("ship-state")["Order"].mean().reset_index()
    fig_avg_state = px.bar(
        state_avg_revenue,
        x="ship-state",
        y="Order",
        color="ship-state",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    st.plotly_chart(fig_avg_state, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row2[1]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">B2B vs Consumer Orders</div>', unsafe_allow_html=True)

    b2b_filter = st.multiselect(
        "Select Business Type",
        options=list(amazon["B2B"].unique()),
        default=list(amazon["B2B"].unique()),
        key="b2b_filter",
    )
    filtered_data = amazon[amazon["B2B"].isin(b2b_filter)]

    b2b_data = filtered_data.groupby("B2B")["Order"].sum().reset_index()
    fig_b2b = px.pie(
        b2b_data,
        names="B2B",
        values="Order",
        color_discrete_sequence=["#1f77b4", "#ff7f0e"],
    )
    st.plotly_chart(fig_b2b, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
