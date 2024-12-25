from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'yoyoyoyoyoyoyyo'  # For flash messages
DATABASE = 'senti.db'

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # To access rows by column name
    return conn

# Home Route
@app.route('/')
def index():
    return render_template('index.html')

# User Registration Route
@app.route('/register/user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        user_data = {
            'fname': request.form['fname'],
            'lname': request.form['lname'],
            'email': request.form['email'],
            'password': request.form['password'],
            'gender': request.form['gender'],
            'height': float(request.form['height']),
            'weight': float(request.form['weight']),
            'dob': request.form['dob'],
            'state': request.form['state'],
            'city': request.form['city']
        }

        # Generate unique UID
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        uid = f"u{cursor.fetchone()[0] + 1:04d}"

        # Check if email already exists
        cursor.execute("SELECT email FROM users WHERE email = ?", (user_data['email'],))
        if cursor.fetchone():
            flash("Email already registered!")
            return redirect(url_for('register_user'))

        # Insert user data
        cursor.execute("""
            INSERT INTO users (uid, fname, lname, email, pwd, gender, height, weight, dob, state, city)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (uid, user_data['fname'], user_data['lname'], user_data['email'], user_data['password'], 
              user_data['gender'], user_data['height'], user_data['weight'], user_data['dob'], 
              user_data['state'], user_data['city']))
        conn.commit()
        conn.close()

        flash("User registered successfully!")
        return redirect(url_for('index'))

    return render_template('regUser.html')

# Company Registration Route
@app.route('/register/company', methods=['GET', 'POST'])
def register_company():
    if request.method == 'POST':
        company_data = {
            'company_name': request.form['company'],
            'email': request.form['email'],
            'password': request.form['password']
        }

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if company email already exists
        cursor.execute("SELECT email FROM companies WHERE email = ?", (company_data['email'],))
        if cursor.fetchone():
            flash("Company with this email already registered!")
            conn.close()
            return redirect(url_for('register_company'))

        # Insert company data
        cursor.execute("""
            INSERT INTO companies (company, email, pwd)
            VALUES (?, ?, ?)
        """, (company_data['company_name'], company_data['email'], company_data['password']))
        conn.commit()
        conn.close()

        flash("Company registered successfully!")
        return redirect(url_for('index'))

    return render_template('regCompany.html')

# User Login Route
@app.route('/login/user', methods=['POST'])
def user_login():
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT uid, fname FROM users WHERE email = ? AND pwd = ?", (email, password))
    result = cursor.fetchone()
    conn.close()

    if result:
        uid = result['uid']
        return redirect(url_for('profile', uid=uid))
    else:
        flash("Invalid credentials, please try again.")
        return redirect(url_for('index'))

# Company Login Route
@app.route('/login/company', methods=['POST'])
def company_login():
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT cid, company FROM companies WHERE email = ? AND pwd = ?", (email, password))
    result = cursor.fetchone()
    conn.close()

    if result:
        cid = result['cid']
        return redirect(url_for('company_profile', cid=cid))
    else:
        flash("Invalid credentials, please try again.")
        return redirect(url_for('index'))

# User Profile Route
@app.route('/user/<uid>')
def profile(uid):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT fname, lname FROM users WHERE uid = ?", (uid,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return "User not found", 404

    cursor.execute("SELECT pid, product FROM products")
    products = cursor.fetchall()

    cursor.execute("""
        SELECT f.feedback, f.sentiment, p.product
        FROM feedback f
        JOIN products p ON f.pid = p.pid
        WHERE f.uid = ?
    """, (uid,))
    feedbacks = cursor.fetchall()

    conn.close()

    return render_template('user.html', user=user, products=products, feedbacks=feedbacks)

# Submit Feedback Route
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    uid = request.form['uid']
    pid = request.form['product']
    feedback = request.form['feedback']

    sentiment = "Neutral"  # Placeholder for sentiment analysis logic

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO feedback (uid, pid, feedback, sentiment)
        VALUES (?, ?, ?, ?)
    """, (uid, pid, feedback, sentiment))
    conn.commit()
    conn.close()

    flash("Feedback submitted successfully!")
    return redirect(url_for('profile', uid=uid))

# Company Profile Route (with Product Viewing)
@app.route('/company/<cid>', methods=['GET', 'POST'])
def company_profile(cid):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get company info
    cursor.execute("SELECT company FROM companies WHERE cid = ?", (cid,))
    company = cursor.fetchone()

    if not company:
        conn.close()
        return "Company not found", 404

    # Get products for this company
    cursor.execute("SELECT pid, product, thumbnail FROM products WHERE cid = ?", (cid,))
    products = cursor.fetchall()

    if request.method == 'POST':
        # Adding a new product
        product_name = request.form['product_name']
        product_thumbnail = request.form['thumbnail_url']

        # Generate unique product ID
        cursor.execute("SELECT COUNT(*) FROM products")
        pid = f"p{cursor.fetchone()[0] + 1:04d}"

        cursor.execute("""
            INSERT INTO products (pid, cid, product, thumbnail)
            VALUES (?, ?, ?, ?)
        """, (pid, cid, product_name, product_thumbnail))
        conn.commit()
        flash("Product added successfully!")
        return redirect(url_for('company_profile', cid=cid))

    conn.close()
    return render_template('company.html', company=company, products=products)



if __name__ == '__main__':
    app.run(debug=True)

