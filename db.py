import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('senti.db')
cursor = conn.cursor()

# 1. Create a new table with the correct schema (timestamp with default value CURRENT_TIMESTAMP)
cursor.execute('''
CREATE TABLE feedback_new (
    fid INTEGER PRIMARY KEY AUTOINCREMENT,
    uid INTEGER,
    pid INTEGER,
    feedback TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    sentiment TEXT,
    FOREIGN KEY (uid) REFERENCES users (uid),
    FOREIGN KEY (pid) REFERENCES products (pid)
)
''')

# 2. Copy data from the old table to the new table
cursor.execute('''
INSERT INTO feedback_new (fid, uid, pid, feedback, timestamp, sentiment)
SELECT fid, uid, pid, feedback, timestamp, sentiment FROM feedback
''')

# 3. Drop the old table
cursor.execute('DROP TABLE feedback')

# 4. Rename the new table to the original table name
cursor.execute('ALTER TABLE feedback_new RENAME TO feedback')

# Commit the changes
conn.commit()

# Example: Insert a new feedback entry (timestamp is automatically set)
uid = 1
pid = 1
feedback = 'Great product!'
sentiment = 'Positive'

cursor.execute('''
INSERT INTO feedback (uid, pid, feedback, sentiment) 
VALUES (?, ?, ?, ?)
''', (uid, pid, feedback, sentiment))

# Commit the new insert
conn.commit()

# Fetch all records to verify the results
cursor.execute('SELECT * FROM feedback')
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
