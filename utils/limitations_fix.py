"""# limitations_fix.py (combine and implement all limitation fixes)

import smtplib
import sqlite3
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import random
from datetime import datetime
import joblib
import numpy as np

# Load ML model
model = joblib.load('models/blockage_rf_model.pkl')

# Weather API key and config
WEATHER_API_KEY = 'your_openweathermap_api_key'
CITY = 'YourCityName'

# Email setup
SENDER_EMAIL = 'aquaflowanalytics2025@gmail.com'
SENDER_PASSWORD = 'ihdc kgyi zgvf tlsw'
RECEIVER_EMAILS = ['aquaflowanalytics2025@gmail.com', 'kankithamadhyastha.com']

def get_weather_condition():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if 'rain' in data.get('weather', [{}])[0]['main'].lower():
            return 'rain'
    except Exception as e:
        print("Weather API failed:", e)
    return 'clear'

def adjust_thresholds_for_weather():
    weather = get_weather_condition()
    if weather == 'rain':
        return {'water_level': 90, 'flow_rate': 45}  # Allow higher values during rain
    return {'water_level': 70, 'flow_rate': 35}      # Normal thresholds

def check_sensor_health(sensor_data):
    faulty = []
    for key, value in sensor_data.items():
        if isinstance(value, (int, float)) and float(value) == 0:
            faulty.append(key)
    return faulty

def send_email_with_snapshot(location, timestamp, sensor):
    explanations = {
        'Water Level': 'Water is overflowing — blockage confirmed.',
        'Flow Rate': 'Unusual low flow suggests debris inside.',
        'Pressure': 'Sudden pressure rise due to clog.',
        'Gas Concentration': 'Hazardous gas detected from block.',
        'Proximity': 'An object is obstructing the pipe.',
        'Vibration': 'Structural vibrations indicate physical disruption.'
    }
    subject = f"🚨 Blockage Detected via {sensor}"
    body = f
    📍 Location: {location}
    ⏰ Time: {timestamp}
    ⚠️ Sensor: {sensor}
    💡 Detail: {explanations.get(sensor, 'Triggered unexpectedly.')}

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = ", ".join(RECEIVER_EMAILS)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach image
    folder = f"static/images/{sensor.lower().replace(' ', '_')}"
    if os.path.exists(folder):
        images = [f for f in os.listdir(folder) if f.endswith(('.jpg', '.png'))]
        if images:
            img = os.path.join(folder, random.choice(images))
            with open(img, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(img)}"')
                msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAILS, msg.as_string())
        print("✅ Email sent.")

def simulate_data():
    # This replaces your get_live_sensor_data function
    from random import uniform, choice, random
    sensors = ['Water Level', 'Flow Rate', 'Pressure', 'Gas Concentration', 'Vibration', 'Proximity']
    triggered = choice(sensors) if random() < 0.2 else '---'
    return {
        'location': 'Zone-' + str(random.randint(1, 10)),
        'water_level': round(uniform(0, 100), 2),
        'flow_rate': round(uniform(0, 50), 2),
        'pressure': round(uniform(0, 200), 2),
        'vibration': round(uniform(0, 10), 2),
        'gas_concentration': round(uniform(0, 100), 2),
        'proximity': round(uniform(0, 20), 2),
        'triggered_sensor': triggered
    }

def main_monitoring_loop():
    data = simulate_data()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    thresholds = adjust_thresholds_for_weather()
    health_issues = check_sensor_health(data)

    if health_issues:
        print("❌ Faulty sensors:", health_issues)

    features = np.array([
        data['water_level'],
        data['flow_rate'],
        data['pressure'],
        data['vibration'],
        data['gas_concentration'],
        data['proximity'],
        0.0
    ]).reshape(1, -1)

    prediction = model.predict(features)[0]
    print("🧠 Prediction:", prediction)

    if prediction == 1 and data['triggered_sensor'] != '---':
        send_email_with_snapshot(data['location'], ts, data['triggered_sensor'])
        insert_history(data['location'], ts, "Blockage Detected", data['triggered_sensor'])
    else:
        insert_history(data['location'], ts, "Blockage Clear", data['triggered_sensor'])

def insert_history(location, ts, status, sensor):
    conn = sqlite3.connect('../database.db')
    c = conn.cursor()
    c.execute("INSERT INTO blockage_history (location, timestamp, status, sensor) VALUES (?, ?, ?, ?)",
              (location, ts, status, sensor))
    conn.commit()
    conn.close()
    print("📥 Logged to DB")

# You can call main_monitoring_loop() every 5 seconds using a scheduler like Celery or APScheduler.
"""
# utils/limitations_fix.py

import requests
from datetime import datetime
import numpy as np
import sqlite3
import joblib
import random

model = joblib.load('models/blockage_rf_model.pkl')

# Weather API key
WEATHER_API_KEY = 'your_openweathermap_api_key'
CITY = 'YourCityName'

def get_weather_condition():
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        if 'rain' in data.get('weather', [{}])[0]['main'].lower():
            return 'rain'
    except Exception as e:
        print("🌧️ Weather API failed:", e)
    return 'clear'

def adjust_thresholds_for_weather():
    weather = get_weather_condition()
    if weather == 'rain':
        return {'water_level': 90, 'flow_rate': 45}
    return {'water_level': 70, 'flow_rate': 35}

def check_sensor_health(sensor_data):
    faulty = []
    for key, value in sensor_data.items():
        if isinstance(value, (int, float)) and float(value) == 0:
            faulty.append(key)
    return faulty

def simulate_data():
    sensors = ['Water Level', 'Flow Rate', 'Pressure', 'Gas Concentration', 'Vibration', 'Proximity']
    triggered = random.choice(sensors) if random.random() < 0.2 else '---'
    return {
        'location': 'Zone-' + str(random.randint(1, 10)),
        'water_level': round(random.uniform(0, 100), 2),
        'flow_rate': round(random.uniform(0, 50), 2),
        'pressure': round(random.uniform(0, 200), 2),
        'vibration': round(random.uniform(0, 10), 2),
        'gas_concentration': round(random.uniform(0, 100), 2),
        'proximity': round(random.uniform(0, 20), 2),
        'triggered_sensor': triggered
    }

def insert_history(location, ts, status, sensor):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO blockage_history (location, timestamp, status, sensor) VALUES (?, ?, ?, ?)",
              (location, ts, status, sensor))
    conn.commit()
    conn.close()
