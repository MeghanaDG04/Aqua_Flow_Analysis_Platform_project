"""# email_alert.py

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_alert_email(location, timestamp):
    sender_email = "your_email@gmail.com"
    receiver_email = "receiver_email@example.com"
    password = "your_email_password"

    subject = "🚨 Drainage Blockage Detected!"
    body = f
    ⚠️ Blockage Alert ⚠️

    A blockage has been detected at:
    📍 Location: {location}
    ⏱️ Time: {timestamp}

    Please take immediate action!


    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
            print("✅ Alert email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
"""
"""from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Email config
SENDER_EMAIL = "aquaflowanalytics2025@gmail.com"
SENDER_PASSWORD = "ihdc kgyi zgvf tlsw"  # Use App Password from Gmail
RECEIVER_EMAIL = "aquaflowanalytics2025@gmail.com"

@app.route('/send-email', methods=['POST'])
def send_alert_email():
    data = request.json
    subject = data.get("subject")
    message = data.get("message")

    try:
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())

        return jsonify({"status": "success", "message": "Email sent successfully!"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
""""""
import os
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_alert_email(location, timestamp, sensor_name):
    sensor_explanations = {
        "Water Level": "Water level has risen significantly, indicating blockage or overflow.",
        "Flow Rate": "Flow is restricted, suggesting possible debris or obstruction.",
        "Pressure": "Abnormally high pressure detected, possibly due to blocked pipes.",
        "Vibration": "Unusual vibrations indicate physical stress in the drainage system.",
        "Gas Concentration": "High gas concentration suggests organic buildup or toxic blockage.",
        "Proximity": "Obstacle detected near the drainage sensor — likely blockage nearby."
    }

    subject = f"🚨 Blockage Alert - {sensor_name} Triggered"
    explanation = sensor_explanations.get(sensor_name, "No explanation available.")

    message_body = f
🚨 Blockage Detected!

📍 Location: {location}
⏰ Time: {timestamp}
🔧 Triggered Sensor: {sensor_name}
📖 Details: {explanation}

Please inspect the area immediately.


    sender_email = "aquaflowanalytics2025@gmail.com"
    receiver_email = "aquaflowanalytics2025@gmail.com"
    password = "ihdc kgyi zgvf tlsw"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message_body, 'plain'))

    # 🔍 Find random image from corresponding folder
    folder_name = sensor_name.replace(" ", "_").lower()  # e.g., water_level
    folder_path = os.path.join("static", "images", folder_name)

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
        if image_files:
            chosen_image = random.choice(image_files)
            full_image_path = os.path.join(folder_path, chosen_image)

            with open(full_image_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{chosen_image}"')
                msg.attach(part)
        else:
            print("⚠️ No images found in folder:", folder_path)
    else:
        print("❌ Folder not found for sensor:", folder_path)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("✅ Email sent with image from folder:", folder_name)
    except Exception as e:
        print("❌ Failed to send email:", e)
"""
import os
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
def send_alert_email(location, timestamp, sensor_name):
    # Don't send email if sensor is not triggered (i.e., '---')
    if sensor_name == "---":
        print("ℹ️ No sensor triggered, email not sent.")
        return

    sensor_explanations = {
        "Water Level": "Water level has risen significantly, indicating blockage or overflow.",
        "Flow Rate": "Flow is restricted, suggesting possible debris or obstruction.",
        "Pressure": "Abnormally high pressure detected, possibly due to blocked pipes.",
        "Vibration": "Unusual vibrations indicate physical stress in the drainage system.",
        "Gas Concentration": "High gas concentration suggests organic buildup or toxic blockage.",
        "Proximity": "Obstacle detected near the drainage sensor — likely blockage nearby.",
        "Pressure/Vibration":" This mainly address about pipie is cracked or any harm to the sysstem ,whch has identified"
    }

    subject = f"🚨 Blockage Alert - {sensor_name} Triggered"
    explanation = sensor_explanations.get(sensor_name, "No explanation available.")

    message_body = f"""
🚨 Blockage Detected!

📍 Location: {location}
⏰ Time: {timestamp}
🔧 Triggered Sensor: {sensor_name}
📖 Details: {explanation}

Please inspect the area immediately.
"""

    sender_email = "aquaflowanalytics2025@gmail.com"
    receiver_email = "aquaflowanalytics2025@gmail.com"
    password = "ihdc kgyi zgvf tlsw"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message_body, 'plain'))

    folder_name = sensor_name.replace(" ", "_").lower()
    folder_path = os.path.join("static", "images", folder_name)

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.png', '.jpeg'))]
        if image_files:
            chosen_image = random.choice(image_files)
            full_image_path = os.path.join(folder_path, chosen_image)

            with open(full_image_path, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename="{chosen_image}"')
                msg.attach(part)
        else:
            print("⚠️ No images found in folder:", folder_path)
    else:
        print("❌ Folder not found for sensor:", folder_path)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("✅ Email sent with image from folder:", folder_name)
    except Exception as e:
        print("❌ Failed to send email:", e)
