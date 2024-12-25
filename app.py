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
def registerUser():
    if request.method == 'POST':
        userData = {
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
        cursor.execute("SELECT email FROM users WHERE email = ?", (userData['email'],))
        if cursor.fetchone():
            flash("Email already registered!")
            return redirect(url_for('registerUser'))

        # Insert user data
        cursor.execute("""
            INSERT INTO users (uid, fname, lname, email, pwd, gender, height, weight, dob, state, city)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (uid, userData['fname'], userData['lname'], userData['email'], userData['password'], 
              userData['gender'], userData['height'], userData['weight'], userData['dob'], 
              userData['state'], userData['city']))
        conn.commit()
        conn.close()

        flash("User registered successfully!")
        return redirect(url_for('index'))

    return render_template('regUser.html')

# Company Registration Route
@app.route('/register/company', methods=['GET', 'POST'])
def registerCompany():
    if request.method == 'POST':
        companyData = {
            'name': request.form['company'],
            'email': request.form['email'],
            'password': request.form['password']
        }

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if company email already exists
        cursor.execute("SELECT email FROM companies WHERE email = ?", (companyData['email'],))
        if cursor.fetchone():
            flash("Company with this email already registered!")
            conn.close()
            return redirect(url_for('registerCompany'))

        # Insert company data
        cursor.execute("""
            INSERT INTO companies (company, email, pwd)
            VALUES (?, ?, ?)
        """, (companyData['name'], companyData['email'], companyData['password']))
        conn.commit()
        conn.close()

        flash("Company registered successfully!")
        return redirect(url_for('index'))

    return render_template('regCompany.html')

# User Login Route
@app.route('/login/user', methods=['POST'])
def userLogin():
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
def companyLogin():
    email = request.form['email']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT cid, company FROM companies WHERE email = ? AND pwd = ?", (email, password))
    result = cursor.fetchone()
    conn.close()

    if result:
        cid = result['cid']
        return redirect(url_for('companyProfile', cid=cid))
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
def submitFeedback():
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
def companyProfile(cid):
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

    # If you need to add sentiment score and feedback count, create new list
    productList = []
    for product in products:
        # Fetch the feedbacks for this product
        cursor.execute("""
            SELECT COUNT(*) as feedback_count, 
                   SUM(CASE WHEN sentiment = 'POSITIVE' THEN 1 ELSE 0 END) AS positive_count
            FROM feedback WHERE pid = ?
        """, (product['pid'],))
        feedbackData = cursor.fetchone()

        # Compute sentiment score as percentage of positive feedback
        totalFeedbacks = feedbackData['feedback_count']
        sentimentScore = (feedbackData['positive_count'] / totalFeedbacks) * 100 if totalFeedbacks > 0 else 0

        # Add sentiment score and feedback count to the product data
        productDict = dict(product)  # Convert Row to dict
        productDict['feedback_count'] = feedbackData['feedback_count']
        productDict['sentiment_score'] = sentimentScore

        productList.append(productDict)

    # Handle new product addition form submission
    if request.method == 'POST':
        productName = request.form['product_name']
        productThumbnail = request.form['thumbnail_url']

        # Generate unique product ID
        cursor.execute("SELECT COUNT(*) FROM products")
        pid = f"p{cursor.fetchone()[0] + 1:04d}"

        cursor.execute("""
            INSERT INTO products (pid, cid, product, thumbnail)
            VALUES (?, ?, ?, ?)
        """, (pid, cid, productName, productThumbnail))
        conn.commit()
        flash("Product added successfully!")
        return redirect(url_for('companyProfile', cid=cid))

    conn.close()
    return render_template('company.html', company=company, products=productList)

from flask import jsonify

@app.route('/feedbacks/<pid>')
def feedbacks(pid):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all feedback for the product
    cursor.execute("""
        SELECT f.fid, f.uid, f.feedback, f.sentiment, f.timestamp, u.email
        FROM feedback f
        JOIN users u ON f.uid = u.uid
        WHERE f.pid = ?
        ORDER BY f.timestamp DESC
    """, (pid,))
    feedbacks = cursor.fetchall()
    conn.close()

    return render_template('feedbacks.html', pid=pid, feedbacks=feedbacks)

# API Endpoint for live updates
@app.route('/api/feedbacks/<pid>', methods=['GET'])
def feedbacks_api(pid):
    sentiment = request.args.get('sentiment')  # Positive, Negative, or All
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    sort_order = request.args.get('sort_order', 'desc')  # asc or desc

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT f.fid, f.uid, f.feedback, f.sentiment, f.timestamp, u.email
        FROM feedback f
        JOIN users u ON f.uid = u.uid
        WHERE f.pid = ?
    """
    params = [pid]

    # Add filters
    if sentiment and sentiment.lower() != 'all':
        query += " AND f.sentiment = ?"
        params.append(sentiment.upper())

    if start_date and end_date:
        query += " AND f.timestamp BETWEEN ? AND ?"
        params.extend([start_date, end_date])

    # Add sorting
    query += f" ORDER BY f.timestamp {sort_order.upper()}"

    cursor.execute(query, params)
    feedbacks = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in feedbacks])

if __name__ == '__main__':
    app.run(debug=True)
