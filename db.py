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
        pid INTEGER PRIMARY KEY AUTOINCREMENT,   -- Auto-increment product ID
        cid INTEGER,                             -- Company ID as foreign key
        product TEXT,                            -- Product name
        thumbnail TEXT,                          -- Product thumbnail image URL
        FOREIGN KEY (cid) REFERENCES companies(cid)  -- Foreign key to companies table
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        fid INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-increment feedback ID
        uid INTEGER,                             -- User ID as foreign key
        pid INTEGER,                             -- Product ID as foreign key
        feedback TEXT,
        sentiment TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Automatically set timestamp
        FOREIGN KEY(uid) REFERENCES users(id),  -- Corrected to reference 'id' from users
        FOREIGN KEY(pid) REFERENCES products(pid) -- Corrected to reference 'pid' from products
    )
''')

# Insert sample data for users
cursor.executemany('''
    INSERT INTO users (uid, fname, lname, email, pwd, gender, height, weight, dob, state, city) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', [
    ("u0001", "Geetu", "Kumari", "geetukumari@gmail.com", "geetu.kumari", "female", 193.24, 63.16, "1996-05-30", "Arunachal Pradesh", "Ziro"),
    ("u0002", "Raj", "Singh", "rajsingh@gmail.com", "raj.singh", "male", 175.50, 75.30, "1994-08-15", "Uttar Pradesh", "Lucknow"),
    ("u0003", "Anjali", "Verma", "anjaliverma@gmail.com", "anjali.verma", "female", 160.75, 55.20, "1997-01-23", "Maharashtra", "Mumbai")
])

# Insert sample data for companies
cursor.executemany('''
    INSERT INTO companies (company, email, pwd) 
    VALUES (?, ?, ?)
''', [
    ("Gucci", "gucci@gmail.com", "gucci"),
    ("Apple", "apple@gmail.com", "apple123"),
    ("Samsung", "samsung@gmail.com", "samsung123")
])

# Insert sample data for products
cursor.executemany('''
    INSERT INTO products (cid, product, thumbnail) 
    VALUES (?, ?, ?)
''', [
    (1, "Essence Mascara Lash Princess", "https://cdn.dummyjson.com/products/images/beauty/Essence%20Mascara%20Lash%20Princess/thumbnail.png"),
    (2, "iPhone 15 Pro Max", "https://cdn.dummyjson.com/products/images/phone/Apple%20iPhone%2015%20Pro%20Max/thumbnail.jpg"),
    (3, "Galaxy S24 Ultra", "https://cdn.dummyjson.com/products/images/phone/Samsung%20Galaxy%20S24%20Ultra/thumbnail.jpg")
])

# Insert sample data for feedback
cursor.executemany('''
    INSERT INTO feedback (uid, pid, feedback, sentiment) 
    VALUES (?, ?, ?, ?)
''', [
    (1, 1, "Great product, highly recommend!", "Positive"),
    (2, 2, "Not as expected, a bit disappointed.", "Negative"),
    (3, 3, "The camera quality is awesome!", "Positive")
])

# Commit changes and close the connection
conn.commit()
conn.close()

print("Tables created and sample data inserted successfully.")
