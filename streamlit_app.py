import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout='wide')
st.title("Vehicle Financial Forecast Dashboard")

# Simulated data based on the provided Excel structure
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

st.sidebar.header("Filters")
selected_year = st.sidebar.multiselect("Select Year", df['Year'].unique(), default=df['Year'].unique())
selected_market = st.sidebar.multiselect("Select Market", df['Market'].unique(), default=df['Market'].unique())
selected_powertrain = st.sidebar.multiselect("Select Powertrain", df['Powertrain'].unique(), default=df['Powertrain'].unique())

filtered_df = df[
    (df['Year'].isin(selected_year)) &
    (df['Market'].isin(selected_market)) &
    (df['Powertrain'].isin(selected_powertrain))
]

st.subheader("Data Overview")
st.dataframe(filtered_df)

st.subheader("Summary Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"₹{filtered_df['Revenue'].sum():,.2f}")
col2.metric("Total Cost", f"₹{filtered_df['TotalCost'].sum():,.2f}")
col3.metric("Total Profit", f"₹{filtered_df['Profit'].sum():,.2f}")

st.subheader("Profit Margin by Market")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=filtered_df, x='Market', y='ProfitMargin', hue='Year', ax=ax)
ax.set_ylabel("Profit Margin (%)")
st.pyplot(fig)

st.subheader("Revenue, Cost and Profit Trends")
melted_df = filtered_df.groupby(['Year'])[['Revenue', 'TotalCost', 'Profit']].sum().reset_index().melt(id_vars='Year')
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(data=melted_df, x='Year', y='value', hue='variable', ax=ax2)
ax2.set_ylabel("Amount (₹)")
st.pyplot(fig2)
