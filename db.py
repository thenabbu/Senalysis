import sqlite3

# Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('senti.db')
cursor = conn.cursor()

# Create tables (adjust according to your actual schema)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        uid INTEGER PRIMARY KEY AUTOINCREMENT,
        fname TEXT,
        lname TEXT,
        email TEXT,
        pwd TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS companies (
        cid INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        email TEXT,
        pwd TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        pid INTEGER PRIMARY KEY AUTOINCREMENT,
        product TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        fid INTEGER PRIMARY KEY AUTOINCREMENT,
        uid INTEGER,
        pid INTEGER,
        feedback TEXT,
        sentiment TEXT,
        FOREIGN KEY(uid) REFERENCES users(uid),
        FOREIGN KEY(pid) REFERENCES products(pid)
    )
''')

conn.commit()
conn.close()
