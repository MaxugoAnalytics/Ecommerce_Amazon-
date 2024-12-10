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

        .visual-box {
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e0e0e0;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }

        .visual-title {
            font-weight: bold;
            font-size: 16px;
            text-align: center;
            color: #232F3E;
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

# Header
st.markdown('<div class="main-header">Amazon Sales Dashboard</div>', unsafe_allow_html=True)

# Key Metrics Section
st.subheader("Key Metrics")
metrics_row = st.columns(4)
metrics_row[0].metric("Total Revenue", f"${amazon['Order'].sum():,.2f}")
metrics_row[1].metric("Total Orders", f"{amazon['Order'].sum():,.0f}")
metrics_row[2].metric("Unique Products", f"{amazon['Style'].nunique():,.0f}")
metrics_row[3].metric("States Covered", f"{amazon['ship-state'].nunique():,.0f}")

# Data Visualizations Section
st.subheader("Data Visualizations")

# Visualization with Filters as Checkboxes
row1 = st.columns(2)

# Helper function to apply checkbox filters
def apply_filter(df, column, selected_values):
    if "All" in selected_values:
        return df
    return df[df[column].isin(selected_values)]

with row1[0]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Orders by Fulfilment Type</div>', unsafe_allow_html=True)

    fulfilment_options = ["All"] + list(amazon["Fulfilment"].unique())
    selected_fulfilments = [
        option for option in fulfilment_options 
        if st.checkbox(option, value=(option == "All"), key=f"fulfilment_{option}")
    ]
    filtered_data = apply_filter(amazon, "Fulfilment", selected_fulfilments)

    fulfilment_data = filtered_data.groupby("Fulfilment")["Order"].sum().reset_index()
    fig_fulfilment = px.pie(
        fulfilment_data,
        names="Fulfilment",
        values="Order",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    st.plotly_chart(fig_fulfilment, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row1[1]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Revenue by Product Style</div>', unsafe_allow_html=True)

    style_options = ["All"] + list(amazon["Style"].unique())
    selected_styles = [
        option for option in style_options 
        if st.checkbox(option, value=(option == "All"), key=f"style_{option}")
    ]
    filtered_data = apply_filter(amazon, "Style", selected_styles)

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

row2 = st.columns(2)

with row2[0]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Orders by Day</div>', unsafe_allow_html=True)

    day_options = ["All"] + list(amazon["Day"].unique())
    selected_days = [
        option for option in day_options 
        if st.checkbox(option, value=(option == "All"), key=f"day_{option}")
    ]
    filtered_data = apply_filter(amazon, "Day", selected_days)

    daily_orders = filtered_data.groupby("Day")["Order"].sum().reset_index()
    fig_day = px.line(
        daily_orders,
        x="Day",
        y="Order",
    )
    st.plotly_chart(fig_day, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row2[1]:
    st.markdown('<div class="visual-box">', unsafe_allow_html=True)
    st.markdown('<div class="visual-title">Average Revenue by State</div>', unsafe_allow_html=True)

    state_options = ["All"] + list(amazon["ship-state"].unique())
    selected_states = [
        option for option in state_options 
        if st.checkbox(option, value=(option == "All"), key=f"state_{option}")
    ]
    filtered_data = apply_filter(amazon, "ship-state", selected_states)

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










