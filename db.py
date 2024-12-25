import sqlite3
import json
import random
from datetime import datetime, timedelta

# Function to generate a random timestamp within the past 2 years
def random_timestamp():
    now = datetime.now()
    two_years_ago = now - timedelta(days=730)
    random_date = two_years_ago + timedelta(days=random.randint(0, 730))
    random_time = datetime.strptime(f"{random.randint(7, 23)}:{random.randint(0, 59)}", "%H:%M").time()
    return datetime.combine(random_date, random_time).strftime("%Y-%m-%d %H:%M:%S")

# Load JSON data
with open('userSQL.json', 'r') as file:
    users = json.load(file)

with open('companySQL.json', 'r') as file:
    companies = json.load(file)

with open('productSQL.json', 'r') as file:
    products = json.load(file)

with open('feedbackSQL.json', 'r') as file:
    feedbacks = json.load(file)

# Connect to SQLite database
conn = sqlite3.connect('senti.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    uid TEXT PRIMARY KEY,
    fname TEXT,
    lname TEXT,
    email TEXT,
    pwd TEXT,
    gender TEXT,
    height REAL,
    weight REAL,
    dob TEXT,
    state TEXT,
    city TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS companies (
    cid TEXT PRIMARY KEY,
    company TEXT,
    email TEXT,
    pwd TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS products (
    pid TEXT PRIMARY KEY,
    cid TEXT,
    product TEXT,
    thumbnail TEXT,
    FOREIGN KEY (cid) REFERENCES companies (cid)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS feedback (
    fid TEXT PRIMARY KEY,
    uid TEXT,
    pid TEXT,
    feedback TEXT,
    timestamp TEXT,
    sentiment TEXT,
    FOREIGN KEY (uid) REFERENCES users (uid),
    FOREIGN KEY (pid) REFERENCES products (pid)
)
''')

# Insert data into tables
for user in users:
    cursor.execute('''
    INSERT INTO users (uid, fname, lname, email, pwd, gender, height, weight, dob, state, city)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user['uid'], user['fname'], user['lname'], user['email'], user['pwd'], user['gender'], user['height'], user['weight'], user['dob'], user['state'], user['city']))

for company in companies:
    cursor.execute('''
    INSERT INTO companies (cid, company, email, pwd)
    VALUES (?, ?, ?, ?)
    ''', (company['cid'], company['company'], company['email'], company['pwd']))

for product in products:
    cursor.execute('''
    INSERT INTO products (pid, cid, product, thumbnail)
    VALUES (?, ?, ?, ?)
    ''', (product['pid'], product['cid'], product['product'], product['thumbnail']))

for feedback in feedbacks:
    cursor.execute('''
    INSERT INTO feedback (fid, uid, pid, feedback, timestamp, sentiment)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (feedback['fid'], feedback['uid'], feedback['pid'], feedback['feedback'], random_timestamp(), feedback['sentiment']))

# Commit and close
conn.commit()
conn.close()