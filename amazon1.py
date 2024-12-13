import streamlit as st
import pandas as pd
import plotly.express as px
import os 

st.set_page_config(page_title="Amazon Sales!!!", layout = "wide")
st.title('Amazon Sales Dashboard by Maxwell Adigwe')
st.markdown('<style>div.block-container{padding-top:lrem;}</style>', unsafe_allow_html=True)

# Load and cache data
@st.cache_data
def load_data():
    url = 'https://drive.google.com/uc?id=1j-6nn-SvsVlw_ySdMa73dbmaa92ehq-Z'
    amazon = pd.read_csv(url)
    return amazon

# Load data
amazon = load_data()

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

# Row 1 (Three Columns with Further Reduced Widths)
row1 = st.columns([0.017, 0.017, 0.017])  # Further reduced column sizes

with row1[0]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Orders by Fulfilment Type</div>', unsafe_allow_html=True)

    fulfilment_filter = st.multiselect(
        "Select Fulfilment Type",
        options=["All"] + list(amazon["Fulfilment"].unique()),
        default="All",
        key="fulfilment_filter",
    )
    filtered_data = amazon if "All" in fulfilment_filter else amazon[amazon["Fulfilment"].isin(fulfilment_filter)]

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
        options=["All"] + list(amazon["Day"].unique()),
        default="All",
        key="day_filter",
    )
    filtered_data = amazon if "All" in day_filter else amazon[amazon["Day"].isin(day_filter)]

    daily_orders = filtered_data.groupby("Day")["Order"].sum().reset_index()
    fig_day = px.line(
        daily_orders,
        x="Day",
        y="Order",
    )
    st.plotly_chart(fig_day, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row1[2]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">B2B vs Consumer Orders</div>', unsafe_allow_html=True)

    b2b_filter = st.multiselect(
        "Select Business Type",
        options=["All"] + list(amazon["B2B"].unique()),
        default="All",
        key="b2b_filter",
    )
    filtered_data = amazon if "All" in b2b_filter else amazon[amazon["B2B"].isin(b2b_filter)]

    b2b_data = filtered_data.groupby("B2B")["Order"].sum().reset_index()
    fig_b2b = px.pie(
        b2b_data,
        names="B2B",
        values="Order",
        color_discrete_sequence=["#1f77b4", "#ff7f0e"],
    )
    st.plotly_chart(fig_b2b, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Row 2 (Three Columns with Further Reduced Widths)
row2 = st.columns([0.017, 0.017, 0.017])  # Further reduced column sizes

with row2[0]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Average Revenue by State</div>', unsafe_allow_html=True)

    state_filter = st.multiselect(
        "Select Shipping State",
        options=["All"] + list(amazon["ship-state"].unique()),
        default="All",
        key="state_filter",
    )
    filtered_data = amazon if "All" in state_filter else amazon[amazon["ship-state"].isin(state_filter)]

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
    st.markdown('<div class="visual-title">Orders by Product Category</div>', unsafe_allow_html=True)

    category_data = filtered_data.groupby("Category")["Order"].sum().reset_index()
    fig_category = px.bar(
        category_data,
        x="Category",
        y="Order",
        color="Category",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    st.plotly_chart(fig_category, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row2[2]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Top 10 States by Revenue</div>', unsafe_allow_html=True)

    top_states = filtered_data.groupby("ship-state")["Order"].sum().reset_index().nlargest(10, "Order")
    fig_top_states = px.bar(
        top_states,
        x="ship-state",
        y="Order",
        color="ship-state",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    st.plotly_chart(fig_top_states, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
