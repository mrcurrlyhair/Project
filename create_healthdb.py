import sqlite3

conn = sqlite3.connect('health.db')
cursor = conn.cursor()


# TESTING 
cursor.execute('''
    CREATE TABLE IF NOT EXISTS health (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        age INTEGER,
        weight REAL,
        blood_type TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

conn.commit()
conn.close()
print("Health database created.")