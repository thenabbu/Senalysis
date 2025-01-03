from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
from transformers import pipeline

app = Flask(__name__)
app.secret_key = "yoyoyoyoyoyoyyo"
DATABASE = "senti.db"
classifier = pipeline("sentiment-analysis")


def dbConnection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def sentiment(feedback_text):
    result = classifier(feedback_text)
    slabel = result[0]["label"]
    return "POSITIVE" if slabel == "POSITIVE" else "NEGATIVE"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register/user", methods=["GET", "POST"])
def registerUser():
    if request.method == "POST":
        data = {
            "fname": request.form["fname"],
            "lname": request.form["lname"],
            "email": request.form["email"],
            "password": request.form["password"],
            "gender": request.form["gender"],
            "dob": request.form["dob"],
            "state": request.form["state"],
            "city": request.form["city"],
        }

        conn = dbConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users WHERE email = ?", (data["email"],))
        if cursor.fetchone():
            flash("Email already registered!")
            conn.close()
            return redirect(url_for("registerUser"))

        cursor.execute(
            """
            INSERT INTO users (fname, lname, email, pwd, gender, dob, state, city)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data["fname"],
                data["lname"],
                data["email"],
                data["password"],
                data["gender"],
                data["dob"],
                data["state"],
                data["city"],
            ),
        )
        conn.commit()
        conn.close()

        flash("User registered successfully!")
        return redirect(url_for("index"))

    return render_template("regUser.html")


@app.route("/register/company", methods=["GET", "POST"])
def registerCompany():
    if request.method == "POST":
        companyData = {
            "name": request.form["company"],
            "email": request.form["email"],
            "password": request.form["password"],
        }

        conn = dbConnection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT email FROM companies WHERE email = ?", (companyData["email"],)
        )
        if cursor.fetchone():
            flash("Company with this email already registered!")
            conn.close()
            return redirect(url_for("registerCompany"))

        cursor.execute(
            """
            INSERT INTO companies (company, email, pwd)
            VALUES (?, ?, ?)
        """,
            (companyData["name"], companyData["email"], companyData["password"]),
        )
        conn.commit()
        conn.close()

        flash("Company registered successfully!")
        return redirect(url_for("index"))

    return render_template("regCompany.html")


@app.route("/login/user", methods=["POST"])
def userLogin():
    email = request.form["email"]
    password = request.form["password"]

    conn = dbConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT uid, fname FROM users WHERE email = ? AND pwd = ?", (email, password)
    )
    result = cursor.fetchone()
    conn.close()

    if result:
        uid = result["uid"]
        return redirect(url_for("profile", uid=uid))
    else:
        flash("Invalid credentials, please try again.")
        return redirect(url_for("index"))


@app.route("/login/company", methods=["POST"])
def companyLogin():
    email = request.form["email"]
    password = request.form["password"]

    conn = dbConnection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT cid, company FROM companies WHERE email = ? AND pwd = ?",
        (email, password),
    )
    result = cursor.fetchone()
    conn.close()

    if result:
        cid = result["cid"]
        return redirect(url_for("companyProfile", cid=cid))
    else:
        flash("Invalid credentials, please try again.")
        return redirect(url_for("index"))


@app.route("/user/<uid>")
def profile(uid):
    conn = dbConnection()
    cursor = conn.cursor()

    cursor.execute("SELECT fname, lname FROM users WHERE uid = ?", (uid,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return "User not found", 404

    cursor.execute("SELECT pid, product FROM products")
    products = cursor.fetchall()

    cursor.execute(
        """
        SELECT f.feedback, f.sentiment, p.product
        FROM feedback f
        JOIN products p ON f.pid = p.pid
        WHERE f.uid = ?
    """,
        (uid,),
    )
    feedbacks = cursor.fetchall()

    conn.close()

    return render_template(
        "user.html", user=user, products=products, feedbacks=feedbacks, uid=uid
    )


@app.route("/submit", methods=["POST"])
def submitFeedback():
    uid = request.form["uid"]
    pid = request.form["product"]
    feedback = request.form["feedback"]

    slabel = sentiment(feedback)

    conn = dbConnection()
    cursor = conn.cursor()

    cursor.execute(
        """ 
        INSERT INTO feedback (uid, pid, feedback, sentiment)
        VALUES (?, ?, ?, ?)
    """,
        (uid, pid, feedback, slabel),
    )
    conn.commit()
    conn.close()

    flash("Feedback submitted successfully!")
    return redirect(url_for("profile", uid=uid))


@app.route("/company/<cid>", methods=["GET", "POST"])
def companyProfile(cid):
    conn = dbConnection()
    cursor = conn.cursor()

    cursor.execute("SELECT company FROM companies WHERE cid = ?", (cid,))
    company = cursor.fetchone()

    if not company:
        conn.close()
        return "Company not found", 404

    cursor.execute("SELECT pid, product, thumbnail FROM products WHERE cid = ?", (cid,))
    products = cursor.fetchall()

    plist = []
    for product in products:

        cursor.execute(
            """
            SELECT COUNT(*) as feedback_count, 
                   SUM(CASE WHEN sentiment = 'POSITIVE' THEN 1 ELSE 0 END) AS positive_count
            FROM feedback WHERE pid = ?
        """,
            (product["pid"],),
        )
        feedbackData = cursor.fetchone()

        totalFeedbacks = feedbackData["feedback_count"]
        sentimentScore = (
            (feedbackData["positive_count"] / totalFeedbacks) * 100
            if totalFeedbacks > 0
            else 0
        )

        productDict = dict(product)
        productDict["feedback_count"] = feedbackData["feedback_count"]
        productDict["sentiment_score"] = sentimentScore

        plist.append(productDict)

    if request.method == "POST":
        productName = request.form["product_name"]
        productThumbnail = request.form["thumbnail_url"]

        conn = dbConnection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO products (cid, product, thumbnail)
            VALUES (?, ?, ?)
        """,
            (cid, productName, productThumbnail),
        )
        conn.commit()
        flash("Product added successfully!")
        return redirect(url_for("companyProfile", cid=cid))

    conn.close()
    return render_template("company.html", company=company, products=plist)


@app.route("/feedbacks/<pid>")
def feedbacks(pid):
    conn = dbConnection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT f.fid, f.uid, f.feedback, f.sentiment, f.timestamp, u.email
        FROM feedback f
        JOIN users u ON f.uid = u.uid
        WHERE f.pid = ?
        ORDER BY f.timestamp DESC
    """,
        (pid,),
    )
    feedbacks = cursor.fetchall()
    conn.close()

    return render_template("feedbacks.html", pid=pid, feedbacks=feedbacks)


@app.route("/api/feedbacks/<pid>", methods=["GET"])
def feedbacks_api(pid):
    sentiment = request.args.get("sentiment")
    sDate = request.args.get("start_date")
    eDate = request.args.get("end_date")
    order = request.args.get("sort_order", "desc")

    conn = dbConnection()
    cursor = conn.cursor()

    query = """
        SELECT f.fid, f.uid, f.feedback, f.sentiment, f.timestamp, u.email
        FROM feedback f
        JOIN users u ON f.uid = u.uid
        WHERE f.pid = ?
    """
    params = [pid]

    if sentiment and sentiment.lower() != "all":
        query += " AND f.sentiment = ?"
        params.append(sentiment.upper())

    if sDate and eDate:
        query += " AND f.timestamp BETWEEN ? AND ?"
        params.extend([sDate, eDate])

    query += f" ORDER BY f.timestamp {order.upper()}"

    cursor.execute(query, params)
    feedbacks = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in feedbacks])


if __name__ == "__main__":
    app.run(debug=True)
