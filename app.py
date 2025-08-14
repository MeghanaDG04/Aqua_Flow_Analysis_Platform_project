from flask import Flask, render_template, request, redirect, url_for, session, flash,jsonify
import joblib
import numpy as np
from datetime import datetime
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from email_alert import send_alert_email
from utils.generate_random_data import get_live_sensor_data
from utils.limitations_fix import (
    adjust_thresholds_for_weather,
    check_sensor_health,
    simulate_data
)
from flask import Response


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

model = joblib.load('models/blockage_rf_model.pkl')

"""def insert_history(location, timestamp, status, sensor_triggered):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO blockage_history (location, timestamp, status, sensor) VALUES (?, ?, ?, ?)",
              (location, timestamp, status, sensor_triggered))
    conn.commit()
    conn.close()
"""
def insert_history(location, timestamp, status, sensor_triggered):
    try:
        with sqlite3.connect('database.db', timeout=5) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO blockage_history (location, timestamp, status, sensor) VALUES (?, ?, ?, ?)",
                      (location, timestamp, status, sensor_triggered))
            conn.commit()
    except sqlite3.OperationalError as e:
        print(f"❌ DB Error: {e}")


def get_history():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM blockage_history ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return rows

@app.route('/')
def splash():
    return render_template('splash.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user[2], password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials", "danger")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        flash("Registered successfully! Please login.", "success")
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/clear_history')
def clear_history():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM blockage_history")
    conn.commit()
    conn.close()
    flash("History cleared successfully.", "success")
    return redirect(url_for('history'))

"""@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    sensor_data = get_live_sensor_data()
    features = np.array([
        sensor_data['water_level'],
        sensor_data['flow_rate'],
        sensor_data['pressure'],
        sensor_data['vibration'],
        sensor_data['gas_concentration'],
        sensor_data['proximity'],
        0.0
    ]).reshape(1, -1)

    prediction = model.predict(features)[0]
    location = sensor_data['location']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    triggered_sensor = sensor_data.get('triggered_sensor','Unknown')

    if prediction == 1:
        status = 'Blockage Detected'
        send_alert_email(location, timestamp)
    else:
        status = 'Clear'

    insert_history(location, timestamp, status, triggered_sensor)

    return render_template('dashboard.html', data=sensor_data, prediction=status)
"""
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    # Live sensor data
    sensor_data = get_live_sensor_data()
    features = np.array([
        sensor_data['water_level'],
        sensor_data['flow_rate'],
        sensor_data['pressure'],
        sensor_data['vibration'],
        sensor_data['gas_concentration'],
        sensor_data['proximity'],
        0.0
    ]).reshape(1, -1)

    prediction = model.predict(features)[0]
    location = sensor_data['location']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    triggered_sensor = sensor_data.get('triggered_sensor','Unknown')

    if prediction == 1:
        status = 'Blockage Detected'
        send_alert_email(location, timestamp,triggered_sensor)
    else:
        status = 'Clear'

    insert_history(location, timestamp, status, triggered_sensor)

    # Fetch history
    history_rows = get_history()

    return render_template(
        'dashboard.html',
        data=sensor_data,
        prediction=status,
        history=history_rows
    )

"""@app.route('/live_data')
def live_data():
    sensor_data = get_live_sensor_data()
    sensor_data = simulate_data()

    triggered_sensor = sensor_data.get('triggered_sensor', '---')
    location = sensor_data.get('location', 'Unknown')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check for specific events like pipe crack or flooding
    pressure = sensor_data.get('pressure', 0)
    water_level = sensor_data.get('water_level', 0)
    vibration = sensor_data.get('vibration', 0)

    # Detect pipe crack (example: pressure drop below a threshold or abnormal vibrations)
    is_pipe_crack = pressure < 20 or vibration > 100
    # Detect flooding (example: water level above a certain threshold)
    is_flooding = water_level > 100

    if is_pipe_crack:
        status = "Pipe Crack Detected"
        send_alert_email(location, timestamp, "Pipe Crack")
    elif is_flooding:
        status = "Flooding Detected"
        send_alert_email(location, timestamp, "Flooding")
    elif triggered_sensor != "---":
        status = "Blockage Detected"
        send_alert_email(location, timestamp, triggered_sensor)
    else:
        status = "Blockage Clear"

    insert_history(location, timestamp, status, triggered_sensor)

    return jsonify({
        "sensor_data": sensor_data,
        "status": status,
        "timestamp": timestamp
    })
"""
"""@app.route('/live_data')
def live_data():
    sensor_data = simulate_data()  # now using smart simulation
    triggered_sensor = sensor_data.get('triggered_sensor', '---')
    location = sensor_data.get('location', 'Unknown')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get smart thresholds based on weather
    thresholds = adjust_thresholds_for_weather()

    # Check for faulty sensors
    faulty = check_sensor_health(sensor_data)
    if faulty:
        print("❌ Faulty sensors detected:", faulty)

    # Detect flooding and pipe crack
    is_flooding = sensor_data['water_level'] > thresholds['water_level']
    is_pipe_crack = sensor_data['pressure'] < 20 or sensor_data['vibration'] > 100

    if is_pipe_crack:
        status = "Pipe Crack Detected"
        send_alert_email(location, timestamp, "Pressure")
    elif is_flooding:
        status = "Flooding Detected"
        send_alert_email(location, timestamp, "Water Level")
    elif triggered_sensor != "---":
        status = "Blockage Detected"
        send_alert_email(location, timestamp, triggered_sensor)
    else:
        status = "Blockage Clear"

    insert_history(location, timestamp, status, triggered_sensor)

    return jsonify({
        "sensor_data": sensor_data,
        "status": status,
        "timestamp": timestamp
    })
"""
from flask import jsonify
import random

"""@app.route('/live_data')
def live_data():
    sensor_data = get_live_sensor_data()

    triggered_sensor = sensor_data.get('triggered_sensor', '---')
    location = sensor_data.get('location', 'Unknown')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Get sensor values
    pressure = sensor_data.get('pressure', 0)
    water_level = sensor_data.get('water_level', 0)
    vibration = sensor_data.get('vibration', 0)

    # 🔍 Rarely simulate flooding or pipe crack — 10% chance
    detect_flooding = random.random() < 0.1 and water_level > 80
    detect_crack = random.random() < 0.1 and (pressure < 15 or vibration > 9)

    # Priority: Pipe crack > Flooding > Blockage > Clear
    if detect_crack:
        status = "Pipe Crack Detected"
        triggered_sensor = "Vibration"
        send_alert_email(location, timestamp, "Vibration")
    elif detect_flooding:
        status = "Flooding Detected"
        triggered_sensor = "Water Level"
        send_alert_email(location, timestamp, "Water Level")
    elif triggered_sensor != "---":
        status = "Blockage Detected"
        send_alert_email(location, timestamp, triggered_sensor)
    else:
        status = "Blockage Clear"

    insert_history(location, timestamp, status, triggered_sensor)

    return jsonify({
        "sensor_data": sensor_data,
        "status": status,
        "timestamp": timestamp
    })"""
"""
import random  # make sure this is imported at the top
@app.route('/live_data')
def live_data():
    sensor_data = get_live_sensor_data()
    thresholds = get_thresholds()

    # Fallback if no config
    water_thresh = float(thresholds.get('water_level', 100))
    pressure_thresh = float(thresholds.get('pressure', 20))
    vibration_thresh = float(thresholds.get('vibration', 100))
    alert_enabled = thresholds.get('alerts', 'on') == 'on'

    triggered_sensor = sensor_data.get('triggered_sensor', '---')
    location = sensor_data.get('location', 'Unknown')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    pressure = sensor_data.get('pressure', 0)
    water_level = sensor_data.get('water_level', 0)
    vibration = sensor_data.get('vibration', 0)

    status = "Blockage Clear"

    if triggered_sensor != "---":
        status = "Blockage Detected"
    elif pressure < pressure_thresh or vibration > vibration_thresh:
        status = "Pipe Crack Detected"
        triggered_sensor = "Pressure/Vibration"
    elif water_level > water_thresh:
        status = "Flooding Detected"
        triggered_sensor = "Water Level"

    if alert_enabled and triggered_sensor != "---":
        send_alert_email(location, timestamp, triggered_sensor)

    insert_history(location, timestamp, status, triggered_sensor)

    return jsonify({
        "sensor_data": sensor_data,
        "status": status,
        "timestamp": timestamp
    })
"""
"""from datetime import datetime, timedelta
import sqlite3

def can_send_alert():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT last_sent FROM alert_log ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()

    if not row:
        return True  # No email ever sent

    last_sent = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
    now = datetime.now()

    # Fetch from settings
    config = get_thresholds_from_config()
    alert_gap = int(config.get('frequency', 5))  # frequency in minutes

    return now - last_sent >= timedelta(minutes=alert_gap)

"""
@app.route('/live_data')
def live_data():
    sensor_data = get_live_sensor_data()
    location = sensor_data.get('location', 'Unknown')
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Extract sensor values
    pressure = sensor_data.get('pressure', 0)
    water_level = sensor_data.get('water_level', 0)
    vibration = sensor_data.get('vibration', 0)
    triggered_sensor = '---'  # default

    # Control detection probabilities
    roll = random.random()  # Generates float between 0 and 1

    if roll < 0.10:  # 10% chance for flooding or pipe crack
        if water_level > 100:
            status = "Flooding Detected"
            triggered_sensor = "Water Level"
        else:
            status = "Pipe Crack Detected"
            triggered_sensor = "Pressure/Vibration"
        send_alert_email(location, timestamp, triggered_sensor)

    elif roll < 0.30:  # Next 20% for blockage
        sensors = ["Water Level", "Flow Rate", "Pressure", "Vibration", "Gas Concentration", "Proximity"]
        triggered_sensor = random.choice(sensors)
        status = "Blockage Detected"
        send_alert_email(location, timestamp, triggered_sensor)

    else:  # Remaining 70% for clear
        status = "Blockage Clear"
        triggered_sensor = "---"

    insert_history(location, timestamp, status, triggered_sensor)

    return jsonify({
        "sensor_data": sensor_data,
        "status": status,
        "timestamp": timestamp
    })
"""
def get_thresholds():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM config LIMIT 1")
    row = c.fetchone()
    conn.close()

    if row:
        keys = ['email', 'frequency', 'water_level', 'flow_rate', 'pressure',
                'vibration', 'gas_concentration', 'proximity', 'alerts']
        return dict(zip(keys, row))
    return {}"""

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        # Get form data
        email = request.form['email']
        frequency = request.form['frequency']
        water_level = request.form['water_level']
        flow_rate = request.form['flow_rate']
        pressure = request.form['pressure']
        vibration = request.form['vibration']
        gas_concentration = request.form['gas_concentration']
        proximity = request.form['proximity']
        alerts = request.form['alerts']

        # Update DB
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("DELETE FROM config")  # Only keep one config row
        c.execute("""INSERT INTO config (email, frequency, water_level, flow_rate, pressure,
                     vibration, gas_concentration, proximity, alerts)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                  (email, frequency, water_level, flow_rate, pressure,
                   vibration, gas_concentration, proximity, alerts))
        conn.commit()
        conn.close()

    # Load existing settings
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM config LIMIT 1")
    row = c.fetchone()
    conn.close()

    if row:
        keys = ['email', 'frequency', 'water_level', 'flow_rate', 'pressure',
                'vibration', 'gas_concentration', 'proximity', 'alerts']
        settings = dict(zip(keys, row))
    else:
        settings = {k: '' for k in ['email', 'frequency', 'water_level', 'flow_rate', 'pressure',
                                    'vibration', 'gas_concentration', 'proximity', 'alerts']}

    return render_template('settings.html', settings=settings)

"""@app.route('/live_data')
def live_data():
    sensor_data = get_live_sensor_data()

    features = np.array([
        sensor_data['water_level'],
        sensor_data['flow_rate'],
        sensor_data['pressure'],
        sensor_data['vibration'],
        sensor_data['gas_concentration'],
        sensor_data['proximity'],
        0.0
    ]).reshape(1, -1)

    prediction = model.predict(features)[0]
    location = sensor_data['location']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    triggered_sensor = sensor_data.get('triggered_sensor', 'Unknown')

    if prediction == 1:
        status = 'Blockage Detected'
        send_alert_email(location, timestamp,triggered_sensor)  # send alert if blocked
    else:
        status = 'Clear'

    insert_history(location, timestamp, status, triggered_sensor)  # store in history

    return {
        "sensor_data": sensor_data,
        "status": status,
        "timestamp": timestamp
    }

"""

@app.route('/history')
def history():
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT id, location, timestamp, status, sensor FROM blockage_history ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()

    return render_template('history.html', rows=rows)

@app.route('/download_history')
def download_history():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM blockage_history")
    rows = c.fetchall()
    conn.close()

    def generate():
        data = ['ID,Location,Timestamp,Status,Sensor\n']
        for row in rows:
            data.append(','.join(str(x) for x in row) + '\n')
        return data

    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=blockage_history.csv"})

@app.route('/help-center')
def help_center():
    return render_template('help_center.html')

@app.route('/report_issue', methods=['POST'])
def report_issue():
    issue = request.form['issue']
    # Save to DB or notify
    flash('Issue submitted successfully!', 'success')
    return redirect('/help-center')

@app.route('/submit_query', methods=['POST'])
def submit_query():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    # Store or email to support team
    flash('Query submitted successfully!', 'success')
    return redirect('/help-center')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')


@app.route('/analytics-data')
def analytics_data():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Sensor Frequency
    c.execute("SELECT sensor, COUNT(*) FROM blockage_history WHERE sensor != '---' GROUP BY sensor")
    sensor_data = c.fetchall()

    # Blockages by Zone
    c.execute("SELECT location, COUNT(*) FROM blockage_history WHERE status = 'Blockage Detected' GROUP BY location")
    zone_data = c.fetchall()

    # Hourly Blockage Pattern
    c.execute("SELECT strftime('%H', timestamp), COUNT(*) FROM blockage_history GROUP BY strftime('%H', timestamp)")
    hour_data = c.fetchall()

    c.execute(
        "SELECT strftime('%Y-%m', timestamp), COUNT(*) FROM blockage_history WHERE status = 'Blockage Detected' GROUP BY strftime('%Y-%m', timestamp)")
    month_data = c.fetchall()

    conn.close()

    return jsonify({
        "sensor": {row[0]: row[1] for row in sensor_data},
        "zone": {row[0]: row[1] for row in zone_data},
        "hourly": {row[0]: row[1] for row in hour_data},
        "monthly": {row[0]: row[1] for row in month_data}
    })


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error.html"), 404



@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
