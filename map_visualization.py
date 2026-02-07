import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import random

st.subheader("Station Map & Congestion (Simulated)")

# Bengaluru center
Bangalore_coords = [12.9716, 77.5946]
m = folium.Map(location=Bangalore_coords, zoom_start=12)

# Simulated stations
stations = [
    {"name": "Station A", "coords": [12.978, 77.640]},
    {"name": "Station B", "coords": [12.960, 77.610]},
    {"name": "Station C", "coords": [12.990, 77.580]},
    {"name": "Station D", "coords": [12.950, 77.630]},
]

# Add colored markers
for s in stations:
    congestion = random.randint(10, 100)
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

# Heatmap
heat_data = [[s["coords"][0], s["coords"][1], random.randint(1,5)] for s in stations]
HeatMap(heat_data).add_to(m)

# Display map in Streamlit
st_data = st_folium(m, width=700, height=500)
