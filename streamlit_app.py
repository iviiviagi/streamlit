import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet

st.set_page_config(layout='wide')
st.title("Vehicle Financial Forecast Dashboard")

# Dummy data (simulate from Excel structure)
data = {
    'Market': ['EU', 'CN', 'US', 'EU', 'CN', 'US'],
    'Powertrain': ['BEV 90kWh EAWD', 'BEV 87kWh ERWD', 'BEV 90kWh ERWD', 'BEV 90kWh EAWD', 'BEV 87kWh ERWD', 'BEV 90kWh ERWD'],
    'Year': [2026, 2026, 2026, 2027, 2027, 2027],
    'Volume': [10000, 8000, 5000, 11000, 8500, 5200],
    'MSRP': [500000, 480000, 470000, 505000, 485000, 475000],
    'OptionPrice': [25000, 20000, 15000, 25000, 20000, 15000],
    'OptionCost': [20000, 18000, 12000, 20000, 18000, 12000],
    'PowertrainCost': [40000, 38000, 36000, 40000, 38000, 36000],
    'BaseCost': [200000]*6
}
df = pd.DataFrame(data)

# Calculations
df['Revenue'] = (df['MSRP'] + df['OptionPrice']) * df['Volume']
df['UnitCost'] = df['BaseCost'] + df['OptionCost'] + df['PowertrainCost']
df['TotalCost'] = df['UnitCost'] * df['Volume']
df['Profit'] = df['Revenue'] - df['TotalCost']
df['ProfitMargin'] = (df['Profit'] / df['Revenue']) * 100
df['Configuration'] = df['Market'] + " | " + df['Powertrain']

# Sidebar filters
st.sidebar.header("Filters")
selected_year = st.sidebar.multiselect("Select Year", df['Year'].unique(), default=df['Year'].unique())
selected_market = st.sidebar.multiselect("Select Market", df['Market'].unique(), default=df['Market'].unique())
selected_powertrain = st.sidebar.multiselect("Select Powertrain", df['Powertrain'].unique(), default=df['Powertrain'].unique())

filtered_df = df[
    (df['Year'].isin(selected_year)) &
    (df['Market'].isin(selected_market)) &
    (df['Powertrain'].isin(selected_powertrain))
]

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Overview", "Profitability by Market", "Cost Breakdown", 
    "YoY Revenue vs Cost", "Margin Heatmap", "Forecast & Sensitivity"
])

# === Overview Tab ===
with tab1:
    st.subheader("Data Overview")
    st.dataframe(filtered_df)

    st.subheader("Summary Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"₹{filtered_df['Revenue'].sum():,.2f}")
    col2.metric("Total Cost", f"₹{filtered_df['TotalCost'].sum():,.2f}")
    col3.metric("Total Profit", f"₹{filtered_df['Profit'].sum():,.2f}")

# === Profitability by Market ===
with tab2:
    st.subheader("Profit by Market and Year")
    profit_by_market = filtered_df.groupby(['Year', 'Market'])['Profit'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=profit_by_market, x='Market', y='Profit', hue='Year', ax=ax)
    ax.set_ylabel("Total Profit (₹)")
    st.pyplot(fig)

# === Cost Breakdown by Powertrain ===
with tab3:
    st.subheader("Cost Breakdown by Powertrain")
    cost_components = ['BaseCost', 'OptionCost', 'PowertrainCost']
    avg_costs = filtered_df.groupby('Powertrain')[cost_components].mean().reset_index()
    melted = avg_costs.melt(id_vars='Powertrain', var_name='CostComponent', value_name='Amount')
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=melted, x='Powertrain', y='Amount', hue='CostComponent', ax=ax2)
    ax2.set_ylabel("Average Unit Cost (₹)")
    st.pyplot(fig2)

# === YoY Revenue vs Cost ===
with tab4:
    st.subheader("Year-over-Year Revenue vs Cost")
    yoy_df = filtered_df.groupby('Year')[['Revenue', 'TotalCost']].sum().reset_index().melt(id_vars='Year')
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=yoy_df, x='Year', y='value', hue='variable', ax=ax3)
    ax3.set_ylabel("Total Amount (₹)")
    st.pyplot(fig3)

# === Profit Margin Heatmap by Configuration ===
with tab5:
    st.subheader("Profit Margin Heatmap")
    pivot = filtered_df.pivot_table(values='ProfitMargin', index='Powertrain', columns='Market', aggfunc='mean')
    fig4, ax4 = plt.subplots(figsize=(8, 6))
    sns.heatmap(pivot, annot=True, cmap='coolwarm', fmt=".1f", ax=ax4)
    ax4.set_title("Profit Margin (%) by Market and Powertrain")
    st.pyplot(fig4)

# === Forecast & Sensitivity ===
with tab6:
    st.subheader("Revenue Forecast Using Prophet")

    forecast_df = df.groupby("Year")[["Revenue"]].sum().reset_index()
    forecast_df.columns = ["ds", "y"]
    forecast_df['ds'] = pd.to_datetime(forecast_df['ds'], format='%Y')

    m = Prophet()
    m.fit(forecast_df)

    future = m.make_future_dataframe(periods=3, freq='Y')
    forecast = m.predict(future)

    fig5 = m.plot(forecast)
    st.pyplot(fig5)

    st.subheader("🔍 Sensitivity Analysis")
    sensitivity_type = st.radio("Select variable to simulate", ["OptionCost", "Volume"])
    multiplier = st.slider("Adjustment Multiplier", 0.5, 2.0, 1.0, 0.1)

    sim_df = filtered_df.copy()
    if sensitivity_type == "OptionCost":
        sim_df['OptionCost'] *= multiplier
    else:
        sim_df['Volume'] = (sim_df['Volume'] * multiplier).astype(int)

    sim_df['UnitCost'] = sim_df['BaseCost'] + sim_df['OptionCost'] + sim_df['PowertrainCost']
    sim_df['TotalCost'] = sim_df['UnitCost'] * sim_df['Volume']
    sim_df['Revenue'] = (sim_df['MSRP'] + sim_df['OptionPrice']) * sim_df['Volume']
    sim_df['Profit'] = sim_df['Revenue'] - sim_df['TotalCost']

    st.metric("Simulated Total Profit", f"₹{sim_df['Profit'].sum():,.2f}")
    st.dataframe(sim_df[['Market', 'Powertrain', 'Year', 'Volume', 'Profit']])
