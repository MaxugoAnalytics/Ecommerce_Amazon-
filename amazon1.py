import streamlit as st
import pandas as pd
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="Amazon Sales Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Styling
st.markdown("""
<style>
[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

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

#######################
# Load data
@st.cache_data
def load_data():
    url = 'https://drive.google.com/uc?id=1j-6nn-SvsVlw_ySdMa73dbmaa92ehq-Z'
    return pd.read_csv(url)

amazon = load_data()

# Add calculated columns
amazon["Revenue per Order"] = amazon["Order"]
amazon["Is Weekend"] = amazon["Day"].isin(["Saturday", "Sunday"])
amazon["Has Promotion"] = amazon["promotion-ids"] != "No Promotion"

#######################
# Sidebar
with st.sidebar:
    st.title("🛒 Amazon Sales Dashboard")
    st.markdown("Filter data for analysis:")
    selected_styles = st.multiselect("Select Product Styles", options=amazon["Style"].unique(), default=amazon["Style"].unique())
    selected_states = st.multiselect("Select Shipping States", options=amazon["ship-state"].unique(), default=amazon["ship-state"].unique())
    selected_fulfilment = st.multiselect("Select Fulfilment Type", options=amazon["Fulfilment"].unique(), default=amazon["Fulfilment"].unique())
    selected_b2b = st.multiselect("Business Type", options=amazon["B2B"].unique(), default=amazon["B2B"].unique())

# Filter data
filtered_data = amazon[
    (amazon["Style"].isin(selected_styles)) &
    (amazon["ship-state"].isin(selected_states)) &
    (amazon["Fulfilment"].isin(selected_fulfilment)) &
    (amazon["B2B"].isin(selected_b2b))
]

#######################
# Dashboard Layout
col = st.columns((2, 6, 2), gap="medium")

with col[0]:
    st.markdown("#### Key Metrics")
    total_revenue = f"${filtered_data['Revenue per Order'].sum():,.2f}"
    total_orders = f"{filtered_data['Order'].sum():,.0f}"
    unique_products = f"{filtered_data['Style'].nunique():,.0f}"
    states_covered = f"{filtered_data['ship-state'].nunique():,.0f}"
    promo_usage = f"{(filtered_data['Has Promotion'].mean() * 100):.2f}%"
    st.metric("Total Revenue", total_revenue)
    st.metric("Total Orders", total_orders)
    st.metric("Unique Products", unique_products)
    st.metric("States Covered", states_covered)
    st.metric("Promotion Usage", promo_usage)

with col[1]:
    st.markdown("#### Visual Analysis")
    st.write("### Revenue by Style")
    style_revenue = filtered_data.groupby("Style")["Revenue per Order"].sum().reset_index()
    fig = px.bar(style_revenue, x="Style", y="Revenue per Order", title="Revenue by Product Style", color="Style", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)

with col[2]:
    st.markdown("#### Top States by Revenue")
    state_revenue = filtered_data.groupby("ship-state")["Revenue per Order"].sum().reset_index().sort_values(by="Revenue per Order", ascending=False)
    st.dataframe(state_revenue)
