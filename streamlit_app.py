import streamlit as st

st.set_page_config(page_title="Car Company Profit Calculator", layout="wide")
st.title("🚗 Car Company Profit & Revenue Simulator")

st.sidebar.header("Adjust Your Business Assumptions")

# Car Sales
num_cars_sold = st.sidebar.slider("Cars Sold per Year", 0, 100_000, 10_000, step=1000)
avg_base_price = st.sidebar.slider("Average Base Price ($)", 10_000, 100_000, 30_000, step=1000)
avg_option_price = st.sidebar.slider("Average Option Add-on ($)", 0, 20_000, 5_000, step=500)
cost_per_car = st.sidebar.slider("Total Cost per Car ($)", 15_000, 90_000, 28_000, step=1000)

# Financing & Leasing
financing_revenue = st.sidebar.slider("Financing & Leasing Revenue per Car ($)", 0, 10_000, 2000)

# After-Sales Services
service_revenue = st.sidebar.slider("After-Sales Services Revenue per Car ($)", 0, 5000, 1000)

# Connected Services
subscription_revenue = st.sidebar.slider("Connected Services (Software/Subscriptions) per Car ($)", 0, 3000, 500)

# Used Car Sales
used_car_profit = st.sidebar.slider("Profit per Used Car ($)", 0, 8000, 3000)
used_cars_sold = st.sidebar.slider("Used Cars Sold per Year", 0, 50_000, 5000, step=500)

# Fleet Sales
fleet_cars_sold = st.sidebar.slider("Fleet Cars Sold", 0, 30_000, 2000)
fleet_profit_per_car = st.sidebar.slider("Profit per Fleet Car ($)", 0, 10_000, 4000)

# Calculations
selling_price = avg_base_price + avg_option_price
profit_per_car = selling_price - cost_per_car

total_revenue = num_cars_sold * selling_price
total_profit = (
    num_cars_sold * (profit_per_car + financing_revenue + service_revenue + subscription_revenue)
    + used_cars_sold * used_car_profit
    + fleet_cars_sold * fleet_profit_per_car
)

# Output
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Revenue", f"${total_revenue:,.0f}")
    st.metric("Profit per New Car", f"${profit_per_car:,.0f}")

with col2:
    st.metric("Used Car Profit", f"${used_cars_sold * used_car_profit:,.0f}")
    st.metric("Fleet Sales Profit", f"${fleet_cars_sold * fleet_profit_per_car:,.0f}")

st.header("💰 Total Estimated Annual Profit")
st.success(f"${total_profit:,.0f}")
