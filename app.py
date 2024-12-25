from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'yoyoyoyoyoyoyyo'  # For flash messages

# Home Route
@app.route('/')
def index():
    return render_template('index.html')

# User Registration Route
@app.route('/register/user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        password = request.form['password']
        
        # Connect to SQLite database
        conn = sqlite3.connect('sentidb.sqlite')
        cursor = conn.cursor()

        # Check if the email already exists
        cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            flash("Email already registered!")
            return redirect(url_for('register_user'))

        # Insert user details into the database
        cursor.execute("""
            INSERT INTO users (fname, lname, email, pwd)
            VALUES (?, ?, ?, ?)
        """, (fname, lname, email, password))
        conn.commit()
        conn.close()

        flash("User registered successfully!")
        return redirect(url_for('index'))

    return render_template('regUser.html')  # Form for user registration

# Company Registration Route
@app.route('/register/company', methods=['GET', 'POST'])
def register_company():
    if request.method == 'POST':
        company_name = request.form['company_name']
        email = request.form['email']
        password = request.form['password']

        # Connect to SQLite database
        conn = sqlite3.connect('sentidb.sqlite')
        cursor = conn.cursor()

        # Check if the email already exists
        cursor.execute("SELECT email FROM companies WHERE email = ?", (email,))
        if cursor.fetchone():
            flash("Email already registered!")
            return redirect(url_for('register_company'))

        # Insert company details into the database
        cursor.execute("""
            INSERT INTO companies (company, email, pwd)
            VALUES (?, ?, ?)
        """, (company_name, email, password))
        conn.commit()
        conn.close()

        flash("Company registered successfully!")
        return redirect(url_for('index'))

    return render_template('regCompany.html')  # Form for company registration

# User Login Route
@app.route('/login/user', methods=['POST'])
def user_login():
    email = request.form['email']
    password = request.form['password']
    
    # Connect to SQLite database
    conn = sqlite3.connect('sentidb.sqlite')
    cursor = conn.cursor()
    
    # Fetch user ID and name
    cursor.execute("SELECT uid, fname FROM users WHERE email = ? AND pwd = ?", (email, password))
    result = cursor.fetchone()
    
    conn.close()

    if result:
        uid = result[0]  # User ID
        return redirect(url_for('profile', uid=uid))
    else:
        flash("Invalid credentials, please try again.")
        return redirect(url_for('index'))

# Company Login Route
@app.route('/login/company', methods=['POST'])
def company_login():
    email = request.form['email']
    password = request.form['password']
    
    # Connect to SQLite database
    conn = sqlite3.connect('sentidb.sqlite')
    cursor = conn.cursor()
    
    # Fetch company ID and name
    cursor.execute("SELECT cid, company FROM companies WHERE email = ? AND pwd = ?", (email, password))
    result = cursor.fetchone()
    
    conn.close()

    if result:
        cid = result[0]  # Company ID
        return redirect(url_for('company_profile', cid=cid))
    else:
        flash("Invalid credentials, please try again.")
        return redirect(url_for('index'))

# User Profile Route
@app.route('/user/<uid>')
def profile(uid):
    # Connect to SQLite database
    conn = sqlite3.connect('sentidb.sqlite')
    cursor = conn.cursor()

    # Fetch user details using UID
    cursor.execute("SELECT fname, lname FROM users WHERE uid = ?", (uid,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return "User not found", 404

    # Fetch available products for feedback
    cursor.execute("SELECT pid, product FROM products")
    products = cursor.fetchall()

    # Fetch user's previous feedbacks
    cursor.execute("""
        SELECT f.feedback, f.sentiment, p.product
        FROM feedback f
        JOIN products p ON f.pid = p.pid
        WHERE f.uid = ?
    """, (uid,))
    feedbacks = cursor.fetchall()

    conn.close()

    return render_template(
        'user.html',
        user=user,
        products=products,
        feedbacks=feedbacks
    )

# Submit Feedback Route
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    uid = request.form['uid']
    pid = request.form['product']
    feedback = request.form['feedback']

    # Analyze feedback sentiment (placeholder for now)
    sentiment = "Neutral"  # Replace with actual sentiment analysis logic

    # Connect to SQLite database
    conn = sqlite3.connect('sentidb.sqlite')
    cursor = conn.cursor()

    # Insert feedback into the database
    cursor.execute("""
        INSERT INTO feedback (uid, pid, feedback, sentiment)
        VALUES (?, ?, ?, ?)
    """, (uid, pid, feedback, sentiment))
    conn.commit()

    conn.close()

    flash("Feedback submitted successfully!")
    return redirect(url_for('profile', uid=uid))

# Company Profile Route
@app.route('/company/<cid>')
def company_profile(cid):
    # Connect to SQLite database
    conn = sqlite3.connect('sentidb.sqlite')
    cursor = conn.cursor()

    # Fetch company details using CID
    cursor.execute("SELECT company FROM companies WHERE cid = ?", (cid,))
    company = cursor.fetchone()

    conn.close()

    if company:
        company_name = company[0]
        return f"Welcome, {company_name}"
    else:
        return "Company not found", 404

if __name__ == '__main__':
    app.run(debug=True)
