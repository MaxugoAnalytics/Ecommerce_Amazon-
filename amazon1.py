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
            margin-bottom: 20px;
            height: 100%;
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

        /* Set equal column widths for 3 visuals in a row */
        .row {
            display: flex;
            justify-content: space-between;
        }

        .col {
            width: 30%;
            padding: 10px;
        }

        .metric-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
        }

        .visual-box {
            height: 300px;
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

# Filters Section
st.subheader("Filters")
fulfilment_filter = st.multiselect(
    "Select Fulfilment Type",
    options=["All"] + list(amazon["Fulfilment"].unique()),
    default=["All"],
    key="fulfilment_filter",
)

style_filter = st.multiselect(
    "Select Product Style",
    options=["All"] + list(amazon["Style"].unique()),
    default=["All"],
    key="style_filter",
)

day_filter = st.multiselect(
    "Select Day",
    options=["All"] + list(amazon["Day"].unique()),
    default=["All"],
    key="day_filter",
)

state_filter = st.multiselect(
    "Select Shipping State",
    options=["All"] + list(amazon["ship-state"].unique()),
    default=["All"],
    key="state_filter",
)

b2b_filter = st.multiselect(
    "Select Business Type",
    options=["All"] + list(amazon["B2B"].unique()),
    default=["All"],
    key="b2b_filter",
)

# Apply Filters
filtered_data = amazon[
    (amazon["Fulfilment"].isin(fulfilment_filter) if "All" not in fulfilment_filter else True) &
    (amazon["Style"].isin(style_filter) if "All" not in style_filter else True) &
    (amazon["Day"].isin(day_filter) if "All" not in day_filter else True) &
    (amazon["ship-state"].isin(state_filter) if "All" not in state_filter else True) &
    (amazon["B2B"].isin(b2b_filter) if "All" not in b2b_filter else True)
]

# Metrics Section
st.subheader("Key Metrics")
metrics_row = st.container()
with metrics_row:
    st.markdown('<div class="metric-row">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    col1.markdown(
        '<div class="metric-box">'
        '<div class="metric-title">Total Revenue</div>'
        f'<div class="metric-value">${filtered_data["Order"].sum():,.2f}</div>'
        '</div>',
        unsafe_allow_html=True
    )
    col2.markdown(
        '<div class="metric-box">'
        '<div class="metric-title">Total Orders</div>'
        f'<div class="metric-value">{filtered_data["Order"].sum():,.0f}</div>'
        '</div>',
        unsafe_allow_html=True
    )
    col3.markdown(
        '<div class="metric-box">'
        '<div class="metric-title">Unique Products</div>'
        f'<div class="metric-value">{filtered_data["Style"].nunique():,.0f}</div>'
        '</div>',
        unsafe_allow_html=True
    )
    col4.markdown(
        '<div class="metric-box">'
        '<div class="metric-title">States Covered</div>'
        f'<div class="metric-value">{filtered_data["ship-state"].nunique():,.0f}</div>'
        '</div>',
        unsafe_allow_html=True
    )
    col5.markdown(
        '<div class="metric-box">'
        '<div class="metric-title">Fulfillment Types</div>'
        f'<div class="metric-value">{filtered_data["Fulfilment"].nunique():,.0f}</div>'
        '</div>',
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Data Visualizations Section
st.subheader("Data Visualizations")
visuals_row = st.container()

with visuals_row:
    st.markdown('<div class="row">', unsafe_allow_html=True)
    
    # Visual 1: Orders by Fulfilment Type
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="visual-box">', unsafe_allow_html=True)
        st.markdown('<div class="visual-title">Orders by Fulfilment Type</div>', unsafe_allow_html=True)
        fulfilment_data = filtered_data.groupby("Fulfilment")["Order"].sum().reset_index()
        fig_fulfilment = px.pie(
            fulfilment_data,
            names="Fulfilment",
            values="Order",
            color_discrete_sequence=px.colors.qualitative.Set3,
        )
        st.plotly_chart(fig_fulfilment, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Visual 2: Revenue by Product Style
    with col2:
        st.markdown('<div class="visual-box">', unsafe_allow_html=True)
        st.markdown('<div class="visual-title">Revenue by Product Style</div>', unsafe_allow_html=True)
        style_data = filtered_data.groupby("Style")["Order"].sum().reset_index()
        fig_style = px.bar(
            style_data,
            x="Style",
            y="Order",
            color="Style",
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        st.plotly_chart(fig_style, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Visual 3: Orders by Day
    with col3:
        st.markdown('<div class="visual-box">', unsafe_allow_html=True)
        st.markdown('<div class="visual-title">Orders by Day</div>', unsafe_allow_html=True)
        daily_orders = filtered_data.groupby("Day")["Order"].sum().reset_index()
        fig_day = px.line(
            daily_orders,
            x="Day",
            y="Order",
        )
        st.plotly_chart(fig_day, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Row 2
    st.markdown('<div class="row">', unsafe_allow_html=True)

    # Visual 4: Average Revenue by State
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="visual-box">', unsafe_allow_html=True)
        st.markdown('<div class="visual-title">Average Revenue by State</div>', unsafe_allow_html=True)
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

    # Visual 5: B2B vs Consumer Orders
    with col2:
        st.markdown('<div class="visual-box">', unsafe_allow_html=True)
        st.markdown('<div class="visual-title">B2B vs Consumer Orders</div>', unsafe_allow_html=True)
        b2b_data = filtered_data.groupby("B2B")["Order"].sum().reset_index()
        fig_b2b = px.pie(
            b2b_data,
            names="B2B",
            values="Order",
            color_discrete_sequence=["#1f77b4", "#ff7f0e"],
        )
        st.plotly_chart(fig_b2b, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)



