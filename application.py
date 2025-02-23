import os
import sqlite3
from flask import Flask, redirect, render_template, request, session, url_for, g
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from werkzeug.middleware.proxy_fix import ProxyFix

from helpers import apology, login_required

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Use the SQLite database from the volume
def get_db():
    if 'db' not in g:
        db_path = os.path.join(os.getcwd(), 'sqlite_db', 'finance.db')
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.route("/")
@login_required
def index():
    return render_template("welcome.html")

@app.route("/exercises")
@login_required
def exercises():
    return render_template("exercises.html")

@app.route("/statistics")
@login_required
def statistics():
    username = session["user"]
    db = get_db()
    usr = db.cursor()
    usr.execute("SELECT * FROM users WHERE username = ?", (username,))
    rows = usr.fetchall()

    user_id = int(rows[0]['id'])
    username = str(rows[0]['username'])
    hash = str(rows[0]['hash'])
    age = int(rows[0]['age'])
    gender = str(rows[0]['gender'])
    weight = float(rows[0]['weight'])
    height = float(rows[0]['height'])

    bmi = weight / (height * height)

    if bmi <= 18.5:
        bmiStatement = 'which means you are underweight.'
    elif bmi > 18.5 and bmi < 25:
        bmiStatement = 'which means you are normal.'
    elif bmi > 25 and bmi < 30:
        bmiStatement = 'overweight.'
    elif bmi > 30:
        bmiStatement = 'which means you are obese.'

    if gender == "male":
        BMR = 66.47 + (13.75 * weight) + (5.0 * height) - (6.75 * age)
    else:
        BMR = 665.09 + (9.56 * weight) + (1.84 * height) - (4.67 * age)

    heightInCm = height * 2.54
    idealWeight = int(heightInCm - 101)

    usr.execute("SELECT * FROM dailyactivity WHERE user = ?", (username,))
    userData = usr.fetchall()

    totalWalked = 0
    totalSleep = 0
    totalJog = 0
    totalCaloriesBurned = 0
    for data in userData:
        steps = int(data['steps'])
        food = str(data['food'])
        jog = int(data['jog'])
        sleep = int(data['sleep'])
        user = str(data['user'])
        calories = int(data['calories'])

        totalWalked += steps
        totalSleep += sleep
        totalJog += jog
        totalCaloriesBurned += calories

    return render_template("statistics.html", bmi=round(bmi, 2), bmiStatement=bmiStatement, userData=userData,
                           totalWalked=totalWalked, BMR=round(BMR, 2), totalSleep=totalSleep, totalJog=totalJog,
                           currentweight=weight, currentheight=height, age=age, idealWeight=idealWeight,
                           totalCaloriesBurned=totalCaloriesBurned)

@app.route("/diet_plans")
@login_required
def diet_plans():
    return render_template("diet_plans.html")

@app.route("/gym_nearby")
@login_required
def gym_nearby():
    return redirect("https://www.google.co.in/maps/search/GYM?hl=en&source=opensearch.html", code=302)

@app.route("/yoga")
@login_required
def yoga():
    return render_template("yoga.html")

@app.route("/addDetails", methods=["GET", "POST"])
@login_required
def addDetails():
    if request.method == "GET":
        return render_template("addDetails.html")
    elif request.method == "POST":
        username = session["user"]
        db = get_db()

        caloriesburn = int((0.42 * int(request.form.get("sleep"))) + (int(request.form.get("jog")) * 100) + (
                    0.05 * int(request.form.get("steps"))))

        if (request.form.get("food") == "chicken"):
            caloriesburn += 199
        elif (request.form.get("food") == "naan"):
            caloriesburn += 137
        elif (request.form.get("food") == "palak paneer"):
            caloriesburn += 300
        elif (request.form.get("food") == "daal"):
            caloriesburn += 166

        db.execute("INSERT INTO dailyactivity (steps, food, jog, sleep, user, calories) VALUES (?,?,?,?,?,?)"
                   , (int(request.form.get("steps")), str(request.form.get("food")), int(request.form.get("jog")),
                      int(request.form.get("sleep")), username, caloriesburn))

        if request.form.get("weight"):
            db.execute("UPDATE users SET weight = (?) WHERE username = (?)"
                       , (float(request.form.get("weight")), username,))

        if request.form.get("height"):
            db.execute("UPDATE users SET height = (?) WHERE username = (?)"
                       , (float(request.form.get("height")), username,))

        db.commit()
        return render_template("welcome.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        username = request.form.get("username")
        db = get_db()
        usr = db.cursor()
        usr.execute("SELECT * FROM users WHERE username =?", (username,))
        rows = usr.fetchall()

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]['hash']):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = int(rows[0]['id'])
        session["user"] = username

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password") or not request.form.get("Re-password"):
            return apology("all the fields are necessary!")
        elif request.form.get("password") != request.form.get("Re-password"):
            return apology("passwords do not match!")

        db = get_db()
        usr = db.cursor()
        usr.execute("SELECT username FROM users")
        rows = usr.fetchall()

        for data in rows:
            if data['username'] == request.form.get("username"):
                return apology("User already Registered")

        db.execute("INSERT INTO users (username, hash, age, gender, weight, height) VALUES(?,?,?,?,?,?)",
                   (str(request.form.get("username")),
                    pwd_context.hash(request.form.get("password")),
                    int(request.form.get("age")),
                    str(request.form.get("gender")),
                    float(request.form.get("weight")),
                    float(request.form.get("height")),))
        db.commit()
        return render_template("login.html")
    else:
        return render_template("register.html")