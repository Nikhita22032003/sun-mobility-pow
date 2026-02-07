import numpy as np

# Simulated inputs
hour = int(input("Enter current hour (0-23): "))
battery_health = float(input("Battery health (0-100%): "))
station_demand = int(input("Current swaps waiting at station: "))

# Simulated electricity tariff (₹ per kWh)
# Cheap at night, expensive in day
if 0 <= hour < 6:
    tariff = 5
elif 6 <= hour < 12:
    tariff = 10
elif 12 <= hour < 18:
    tariff = 15
else:
    tariff = 8

# Simulated solar output (kWh)
if 6 <= hour < 18:
    solar = np.random.randint(5, 20)  # sunny day
else:
    solar = 0  # night

# Decision logic
if tariff > 12 and solar < 5:
    action = "Swap battery instead of charging now"
elif battery_health < 20:
    action = "Charge battery immediately"
else:
    action = "Charge battery using solar/cheap tariff"

print("\n--- ENERGY OPTIMIZATION DECISION ---")
print(f"Hour: {hour}")
print(f"Tariff: ₹{tariff}/kWh")
print(f"Solar available: {solar} kWh")
print(f"Station demand: {station_demand}")
print(f"Battery health: {battery_health}%")
print(f"Suggested action: {action}")
