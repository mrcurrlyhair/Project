import sqlite3

con = sqlite3.connect('users.db')
cursor = con.cursor()

# create user db
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

con.commit()
con.close()
print("user database created")


con = sqlite3.connect('health.db')
cursor = con.cursor()

# create health db 
cursor.execute('''
    CREATE TABLE IF NOT EXISTS health (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        age INTEGER,
        gender TEXT,
        county TEXT,
        smoking_status TEXT,
        BMI REAL,
        height REAL,
        weight REAL,
        alcohol_use TEXT,
        physical_activity TEXT,
        diet_quality TEXT,
        sleep_hours REAL,
        heart_rate REAL,
        respiratory_rate REAL,
        systolic_bp REAL,
        diastolic_bp REAL
        radon_level INTEGER,
        pollution_level REAL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

con.commit()
con.close()
print("health database created")