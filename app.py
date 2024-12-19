from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flash messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:navya@localhost/sentidb'
db = SQLAlchemy(app)

# Home Route
@app.route('/')
def index():
    return render_template('index.html')

# User Login Route
@app.route('/login/user', methods=['POST'])
def user_login():
    email = request.form['email']
    password = request.form['password']
    
    # Fetch user ID and name
    result = db.session.execute(
        text("SELECT uid, fname FROM users WHERE email = :email AND pwd = :password"),
        {"email": email, "password": password}
    ).fetchone()

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
    
    # Fetch company ID and name
    result = db.session.execute(
        text("SELECT cid, company FROM companies WHERE email = :email AND pwd = :password"),
        {"email": email, "password": password}
    ).fetchone()

    if result:
        cid = result[0]  # Company ID
        return redirect(url_for('company_profile', cid=cid))
    else:
        flash("Invalid credentials, please try again.")
        return redirect(url_for('index'))

# User Profile Route
@app.route('/user/<uid>')
def profile(uid):
    # Fetch user details using UID
    user = db.session.execute(
        text("SELECT fname, lname FROM users WHERE uid = :uid"),
        {"uid": uid}
    ).fetchone()

    if user:
        fname, lname = user
        return f"Welcome, {fname} {lname}"
    else:
        return "User not found", 404

# Company Profile Route
@app.route('/company/<cid>')
def company_profile(cid):
    # Fetch company details using CID
    company = db.session.execute(
        text("SELECT company FROM companies WHERE cid = :cid"),
        {"cid": cid}
    ).fetchone()

    if company:
        company_name = company[0]
        return f"Welcome, {company_name}"
    else:
        return "Company not found", 404

if __name__ == '__main__':
    app.run(debug=True)