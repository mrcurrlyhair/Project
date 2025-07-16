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
        age BLOB,
        gender BLOB,
        county BLOB,
        smoking_status BLOB,
        BMI BLOB,
        height BLOB,
        weight BLOB,
        alcohol_use BLOB,
        physical_activity BLOB,
        diet_quality BLOB,
        sleep_hours BLOB,
        heart_rate BLOB,
        respiratory_rate BLOB,
        systolic_bp BLOB,
        diastolic_bp BLOB,
        radon_level BLOB,
        pollution_level BLOB,
        cholesterol BLOB,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

con.commit()
con.close()
print("health database created")