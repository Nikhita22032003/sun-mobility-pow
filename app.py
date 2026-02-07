import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import numpy as np
import random
import pandas as pd
import joblib

st.set_page_config(page_title="Battery Swap Dashboard", layout="wide")
st.title("🔋 Battery Swap Optimization Dashboard (Learning Prototype)")

st.caption("Uses fully simulated Bengaluru data for learning purposes only.")

# ----------------------------
# 1️⃣ ROI Calculator
# ----------------------------
st.header("1️⃣ ROI Calculator (Simulated)")

fleet_size = st.slider("Number of vehicles in fleet", 10, 500, 50)
swaps_per_day = st.slider("Swaps per vehicle per day", 1, 5, 2)
avg_wait_time = st.slider("Average wait time per swap (minutes)", 1, 30, 10)
cost_per_minute = st.slider("Cost per minute (₹)", 1, 10, 2)

baseline_wait = fleet_size * swaps_per_day * avg_wait_time
optimized_wait = baseline_wait * 0.7  # assume 30% reduction

time_saved = baseline_wait - optimized_wait
money_saved_per_day = time_saved * cost_per_minute
money_saved_per_month = money_saved_per_day * 30

st.subheader("Results")
st.write("Time saved per day (minutes):", round(time_saved, 2))
st.write("Money saved per day (₹):", round(money_saved_per_day, 2))
st.write("Money saved per month (₹):", round(money_saved_per_month, 2))

# ----------------------------
# 2️⃣ Energy Optimization Logic
# ----------------------------
st.header("2️⃣ Energy Optimization Suggestion (Simulated)")

hour = st.slider("Current hour (0-23)", 0, 23, 14)
battery_health = st.slider("Battery health (%)", 0, 100, 60)
station_demand = st.slider("Current swaps waiting at station", 0, 20, 3)

if 0 <= hour < 6:
    tariff = 5
elif 6 <= hour < 12:
    tariff = 10
elif 12 <= hour < 18:
    tariff = 15
else:
    tariff = 8

if "solar" not in st.session_state or st.session_state.get("hour") != hour:
    st.session_state.hour = hour
    if 6 <= hour < 18:
        st.session_state.solar = random.randint(5, 20)
    else:
        st.session_state.solar = 0

solar = st.session_state.solar

if tariff > 12 and solar < 5:
    action = "Swap battery instead of charging now"
elif battery_health < 20:
    action = "Charge battery immediately"
else:
    action = "Charge battery using solar / cheap tariff"

st.subheader("Energy Decision")
st.write(f"Tariff: ₹{tariff}/kWh")
st.write(f"Solar available: {solar} kWh")
st.write(f"Suggested action: **{action}**")

# ----------------------------
# 3️⃣ Map Visualization
# ----------------------------
st.header("3️⃣ Bengaluru Station Map (Simulated)")

Bangalore_coords = [12.9716, 77.5946]
m = folium.Map(location=Bangalore_coords, zoom_start=12)

stations = [
    {"name": "Station A", "coords": [12.978, 77.640]},
    {"name": "Station B", "coords": [12.960, 77.610]},
    {"name": "Station C", "coords": [12.990, 77.580]},
    {"name": "Station D", "coords": [12.950, 77.630]},
]

if "congestion" not in st.session_state:
    st.session_state.congestion = {}
    for s in stations:
        st.session_state.congestion[s["name"]] = random.randint(10, 100)

for s in stations:
    congestion = st.session_state.congestion[s["name"]]
    if congestion < 40:
        color = "green"
    elif congestion < 70:
        color = "orange"
    else:
        color = "red"

    folium.CircleMarker(
        location=s["coords"],
        radius=10,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=f"{s['name']} - Congestion {congestion}%",
    ).add_to(m)

if "heat" not in st.session_state:
    st.session_state.heat = [[s["coords"][0], s["coords"][1], random.randint(1,5)] for s in stations]

HeatMap(st.session_state.heat).add_to(m)

st_folium(m, width=700, height=500)

# ----------------------------
# 4️⃣ ML Wait Time Prediction
# ----------------------------
st.header("4️⃣ ML Wait Time Prediction")

df = pd.read_csv("data/simulated_data.csv")
model = joblib.load("wait_time_model.pkl")

hour_ml = st.slider("Hour of Day", 0, 23, 12, key="ml_hour")
traffic = st.slider("Traffic Level (1-10)", 1, 10, 5)
riders = st.slider("Rider Demand", 5, 100, 30)
tariff_ml = st.selectbox("Electricity Tariff (₹)", [4,6,8])
solar_ml = st.slider("Solar Power (kW)", 0, 25, 10)

input_df = pd.DataFrame([[hour_ml, traffic, riders, tariff_ml, solar_ml]],
                        columns=["hour","traffic_level","rider_demand","tariff_rs","solar_kw"])

if st.button("Predict Wait Time"):
    prediction = model.predict(input_df)[0]
    st.success(f"Predicted Wait Time: {round(prediction,2)} minutes")

st.subheader("Sample Simulated Data")
st.dataframe(df.head())
