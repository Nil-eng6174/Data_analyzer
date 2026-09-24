import streamlit as st
import pandas as pd
import plotly.express as px
from src.analysis import load_data, calculate_kpis, get_revenue_profit_trend, get_category_trend
from src.forecasting import train_forecast_model, generate_future_forecast
from src.insights import generate_insights

st.set_page_config(page_title="Superstore BI Dashboard", layout="wide")

@st.cache_data
def get_data():
    return load_data('data/cleaned_dataset.csv')

df = get_data()

st.title("📊 AI-Powered Business Intelligence & Data Analytics Dashboard")
st.markdown("A complete data pipeline from Data to Actionable Insights.")

# Sidebar Filters
st.sidebar.header("Filters")
min_date = df['order_date'].min()
max_date = df['order_date'].max()

# Year filter instead of date_input to avoid complex type issues
year_list = sorted(df['order_date'].dt.year.unique())
selected_years = st.sidebar.multiselect("Select Year(s)", year_list, default=year_list)

regions = st.sidebar.multiselect("Select Region", df['region'].unique(), default=df['region'].unique())
categories = st.sidebar.multiselect("Select Category", df['category'].unique(), default=df['category'].unique())

# Filter data
filtered_df = df[
    (df['order_date'].dt.year.isin(selected_years)) &
    (df['region'].isin(regions)) &
    (df['category'].isin(categories))
]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# --- KPIs ---
st.header("1. Key Performance Indicators (KPIs)")
kpis = calculate_kpis(filtered_df)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${kpis['Total Revenue']:,.2f}")
col2.metric("Total Profit", f"${kpis['Total Profit']:,.2f}")
col3.metric("Profit Margin", f"{kpis['Profit Margin']:.2f}%")
col4.metric("Total Orders", f"{kpis['Total Orders']:,}")

# --- TREND ANALYSIS ---
st.header("2. Trend Analysis")
trend_df = get_revenue_profit_trend(filtered_df, 'M')
fig_trend = px.line(trend_df, x='order_date', y=['sales', 'profit'], title="Revenue vs Profit Over Time")
st.plotly_chart(fig_trend, use_container_width=True)

# --- DRIVER ANALYSIS ---
st.header("3. Driver Analysis")
col_a, col_b = st.columns(2)
with col_a:
    # Category Performance
    cat_df = filtered_df.groupby('category')['sales'].sum().reset_index()
    fig_cat = px.pie(cat_df, values='sales', names='category', title="Sales by Category")
    st.plotly_chart(fig_cat, use_container_width=True)

with col_b:
    # Region Performance
    reg_df = filtered_df.groupby('region')['profit'].sum().reset_index()
    fig_reg = px.bar(reg_df, x='region', y='profit', title="Profit by Region", color='profit', color_continuous_scale='RdYlGn')
    st.plotly_chart(fig_reg, use_container_width=True)

# --- FORECASTING ---
st.header("4. Predictive Analytics (Forecasting)")
try:
    model, metrics, monthly_data = train_forecast_model(filtered_df)
    future_forecast = generate_future_forecast(model, monthly_data['time_idx'].max(), monthly_data['order_date'].max())
    
    st.write(f"**Model Performance:** R² Score = {metrics['R2']:.2f} | RMSE = ${metrics['RMSE']:,.2f}")
    
    # Plot forecast
    fig_forecast = px.line(monthly_data, x='order_date', y='sales', title="Historical Sales vs 6-Month Forecast")
    fig_forecast.add_scatter(x=future_forecast['order_date'], y=future_forecast['predicted_sales'], mode='lines', name='Forecast', line=dict(dash='dash', color='red'))
    st.plotly_chart(fig_forecast, use_container_width=True)
except Exception as e:
    st.warning("Not enough data points to generate a reliable forecast. Please adjust filters.")

# --- AI INSIGHTS ---
st.header("5. AI-Generated Insights & Actionable Recommendations")
insights = generate_insights(filtered_df)

for i, insight in enumerate(insights):
    with st.expander(f"Insight #{i+1}: {insight['RISK/OPPORTUNITY']}"):
        st.write(f"**Observation:** {insight['OBSERVATION']}")
        st.write(f"**Driver:** {insight['DRIVER']}")
        st.write(f"**Recommendation:** {insight['RECOMMENDATION']}")
