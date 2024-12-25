import sqlite3

# Connect to SQLite database (it will create the file if it doesn't exist)
conn = sqlite3.connect('senti.db')
cursor = conn.cursor()

# Create tables (adjusted schema to keep id as autoincrementing primary key)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uid TEXT UNIQUE,
        fname TEXT,
        lname TEXT,
        email TEXT UNIQUE,
        pwd TEXT,
        gender TEXT,
        height REAL,
        weight REAL,
        dob DATE,
        state TEXT,
        city TEXT
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
