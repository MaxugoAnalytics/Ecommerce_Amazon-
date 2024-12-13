import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Amazon Sales!!!", page_icon=":bar_chart:", layout="wide")

# Move the title to the top corner using inline CSS
st.markdown(
    """
    <style>
        .title-container {
            position: absolute;
            top: 10px; 
            left: 10px; 
            font-size: 24px;
            font-weight: bold;
            color: #232F3E;
            z-index: 1;
        }
    </style>
    <div class="title-container">:bar_chart: Amazon Sales Dashboard by Maxwell Adigwe</div>
    """,
    unsafe_allow_html=True,
)

# Load and cache data
@st.cache_data
def load_data():
    url = 'https://drive.google.com/uc?id=1j-6nn-SvsVlw_ySdMa73dbmaa92ehq-Z'
    amazon = pd.read_csv(url)
    return amazon

# Load data
amazon = load_data()

# Key Metrics Section
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

# Visualization Section
st.subheader("Data Visualizations")

# Example Visualization
row1 = st.columns(3)
with row1[0]:
    st.markdown("### Orders by Fulfilment Type")
    fulfilment_data = amazon.groupby("Fulfilment")["Order"].sum().reset_index()
    fig_fulfilment = px.pie(
        fulfilment_data,
        names="Fulfilment",
        values="Order",
        title="",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    st.plotly_chart(fig_fulfilment, use_container_width=True)

