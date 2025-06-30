import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create user db
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
print("User database created")