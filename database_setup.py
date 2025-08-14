import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Users Table
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
''')

# Blockage History Table
c.execute('''
    CREATE TABLE IF NOT EXISTS blockage_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT,
        timestamp TEXT,
        status TEXT,
        sensor TEXT
    )
''')

# Config Table for Settings
c.execute('''
    CREATE TABLE IF NOT EXISTS config (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        alert_frequency INTEGER,
        vibration_threshold REAL,
        gas_threshold REAL,
        proximity_threshold REAL
    )
''')

# Insert default config row if not present
c.execute("SELECT COUNT(*) FROM config")
if c.fetchone()[0] == 0:
    c.execute('''
        INSERT INTO config (email, alert_frequency, vibration_threshold, gas_threshold, proximity_threshold)
        VALUES (?, ?, ?, ?, ?)
    ''', ("admin@example.com", 1, 5.0, 50.0, 10.0))

conn.commit()
conn.close()

print("✅ Database tables and config initialized.")
