import sqlite3

conn = sqlite3.connect('health.db')
cursor = conn.cursor()


cursor.execute('''
    CREATE TABLE IF NOT EXISTS health (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        age INTEGER,
        gender TEXT,
        postcode TEXT,
        smoking_status TEXT,
        BMI REAL,
        alcohol_use TEXT,
        physical_activity TEXT,
        diet_quality TEXT,
        sleep_hours REAL,
        county_name TEXT,
        radon_level INTEGER,
        pollution REAL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

conn.commit()
conn.close()
print("Health database created.")