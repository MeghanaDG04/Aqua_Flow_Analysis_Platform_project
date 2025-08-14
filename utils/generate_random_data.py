

import random
import csv
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Any

# Real-world example locations (latitude, longitude)
locations = [
    (12.9715, 77.5973),  # Bangalore
    (28.6139, 77.2090),  # Delhi
    (19.0760, 72.8777),  # Mumbai
    (13.0827, 80.2707),  # Chennai
    (22.5726, 88.3639),  # Kolkata
]


# Function to generate historical/bulk data
def generate_random_sensor_data(num_entries: int = 100) -> List[List[Any]]:
    data = []
    current_time = datetime.now()

    for _ in range(num_entries):
        timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")
        location = random.choice(locations)
        water_level = round(random.uniform(0.5, 5.0), 2)
        flow_rate = round(random.uniform(0.1, 3.0), 2)
        pressure = round(random.uniform(0.5, 2.0), 2)
        vibration = round(random.uniform(0.0, 1.0), 2)
        gas_concentration = round(random.uniform(0.0, 100.0), 2)
        proximity = round(random.uniform(0.0, 1.0), 2)
        blockage_status = random.choice([0, 1])  # 0 = No Blockage, 1 = Blockage

        data.append([
            timestamp,
            f"{location[0]},{location[1]}",
            water_level,
            flow_rate,
            pressure,
            vibration,
            gas_concentration,
            proximity,
            blockage_status
        ])

        current_time += timedelta(seconds=5)

    return data


# Function to save data into CSV
def save_to_csv(data: List[List[Any]], filename: str = "sensor_data.csv") -> None:
    headers = [
        "timestamp", "location", "water_level", "flow_rate",
        "pressure", "vibration", "gas_concentration", "proximity", "blockage_status"
    ]
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)


# Real-time single entry simulation for live dashboard
"""def get_live_sensor_data() -> Dict[str, Any]:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    location = random.choice(locations)
    water_level = round(random.uniform(0.5, 5.0), 2)
    flow_rate = round(random.uniform(0.1, 3.0), 2)
    pressure = round(random.uniform(0.5, 2.0), 2)
    vibration = round(random.uniform(0.0, 1.0), 2)
    gas_concentration = round(random.uniform(0.0, 100.0), 2)
    proximity = round(random.uniform(0.0, 1.0), 2)
    blockage_status = random.choice([0, 1])

    triggered_sensors = []
    if blockage_status == 1:
        thresholds = {
            "water_level": 4.0,
            "flow_rate": 2.5,
            "pressure": 1.8,
            "vibration": 0.9,
            "gas_concentration": 90.0,
            "proximity": 0.9
        }

        # Check each sensor against its threshold
        if water_level > thresholds["water_level"]:
            triggered_sensors.append("water_level")
        if flow_rate > thresholds["flow_rate"]:
            triggered_sensors.append("flow_rate")
        if pressure > thresholds["pressure"]:
            triggered_sensors.append("pressure")
        if vibration > thresholds["vibration"]:
            triggered_sensors.append("vibration")
        if gas_concentration > thresholds["gas_concentration"]:
            triggered_sensors.append("gas_concentration")
        if proximity > thresholds["proximity"]:
            triggered_sensors.append("proximity")

    return {
        "timestamp": timestamp,
        "location": f"{location[0]},{location[1]}",
        "water_level": water_level,
        "flow_rate": flow_rate,
        "pressure": pressure,
        "vibration": vibration,
        "gas_concentration": gas_concentration,
        "proximity": proximity,
        "blockage_status": blockage_status,
        "triggered_sensors": triggered_sensors if triggered_sensors else None
    }
"""
"""def get_live_sensor_data():
    sensors = ['Water Level', 'Flow Rate', 'Pressure', 'Vibration', 'Gas Concentration', 'Proximity']
    is_blockage = random.random() < 0.2
    triggered_sensor = random.choice(sensors) if is_blockage else "---"
    return {
        "location": f"Zone-{random.randint(1, 10)}",
        "water_level": round(random.uniform(0, 100), 2),
        "flow_rate": round(random.uniform(0, 50), 2),
        "pressure": round(random.uniform(0, 200), 2),
        "vibration": round(random.uniform(0, 10), 2),
        "gas_concentration": round(random.uniform(0, 100), 2),
        "proximity": round(random.uniform(0, 20), 2),
        "triggered_sensor": triggered_sensor
    }
""""""
import random


def get_live_sensor_data():
    sensors = ['Water Level', 'Flow Rate', 'Pressure', 'Vibration', 'Gas Concentration', 'Proximity']

    # Generate random sensor readings
    data = {
        "location": f"Zone-{random.randint(1, 10)}",
        "water_level": round(random.uniform(0, 100), 2),
        "flow_rate": round(random.uniform(0, 50), 2),
        "pressure": round(random.uniform(0, 200), 2),
        "vibration": round(random.uniform(0, 10), 2),
        "gas_concentration": round(random.uniform(0, 100), 2),
        "proximity": round(random.uniform(0, 20), 2),
    }

    # If any sensor exceeds threshold, we treat it as blockage
    thresholds = {
        'water_level': 80,
        'flow_rate': 40,
        'pressure': 150,
        'vibration': 8,
        'gas_concentration': 90,
        'proximity': 15
    }

    for key, threshold in thresholds.items():
        if data[key] > threshold:
            data["triggered_sensor"] = key.replace("_", " ").title()
            return data  # Return immediately if any sensor triggers

    data["triggered_sensor"] = "---"  # No blockage
    return data
"""
import random


def get_live_sensor_data():
    sensors = ['Water Level', 'Flow Rate', 'Pressure', 'Vibration', 'Gas Concentration', 'Proximity']

    is_blockage = random.random() < 0.2  # 20% chance of blockage
    triggered_sensor = random.choice(sensors) if is_blockage else '---'

    sensor_data = {
        'location': f'Zone-{random.randint(1, 10)}',
        'water_level': round(random.uniform(10, 100), 2),
        'flow_rate': round(random.uniform(0, 50), 2),
        'pressure': round(random.uniform(50, 200), 2),
        'vibration': round(random.uniform(0, 10), 2),
        'gas_concentration': round(random.uniform(0, 100), 2),
        'proximity': round(random.uniform(0, 20), 2),
        'triggered_sensor': triggered_sensor
    }

    return sensor_data


"""import random

def get_live_sensor_data():
    sensors = ['Water Level', 'Flow Rate', 'Pressure', 'Vibration', 'Gas Concentration', 'Proximity']
    is_blockage = random.random() < 0.2  # 20% chance for blockage
    triggered_sensor = random.choice(sensors) if is_blockage else '---'

    return {
        'location': f'Zone-{random.randint(1, 10)}',
        'water_level': round(random.uniform(0, 100), 2),
        'flow_rate': round(random.uniform(0, 50), 2),
        'pressure': round(random.uniform(0, 200), 2),
        'vibration': round(random.uniform(0, 10), 2),
        'gas_concentration': round(random.uniform(0, 100), 2),
        'proximity': round(random.uniform(0, 20), 2),
        'triggered_sensor': triggered_sensor
    }

"""
# Main execution block
if __name__ == "__main__":
    data = generate_random_sensor_data(500)
    save_to_csv(data)
    print("✅ 500 sensor data entries generated and saved to 'sensor_data.csv'")

    # Example live data
    live_data = get_live_sensor_data()
    print("Live Sensor Data Example:")
    print(live_data)
