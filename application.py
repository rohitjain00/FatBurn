import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp


from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = sqlite3.connect("finance.db")

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
    usr = db.cursor()
    usr.execute("SELECT * FROM users WHERE username = ?",(username,))
    rows = usr.fetchall()

    bmi = rows[0][4]/(rows[0][3]* rows[0][3])
    age = rows[0][5]

    if bmi <= 18.5:
        bmiStatement = 'which means you are underweight.'

    elif bmi > 18.5 and bmi < 25:
        bmiStatement = 'which means you are normal.'

    elif bmi > 25 and bmi < 30:
        bmiStatement = 'overweight.'

    elif bmi > 30:
        bmiStatement = 'which means you are obese.'

    if rows[0][6] == "male":
        BMR = 66.47 + (13.75 * rows[0][4]) + (5.0 * rows[0][3]) - (6.75 * age)
    else :
        BMR = 665.09 + (9.56 * rows[0][4]) + (1.84 * rows[0][3]) - (4.67 * age)

    heightInCm = rows[0][3] * 2.54
    idealWeight = int(heightInCm - 101)

    usr.execute("SELECT * FROM dailyactivity WHERE user = ?",(username,))
    userData = usr.fetchall()

    totalWalked = 0
    totalSleep = 0
    totalJog = 0
    totalCaloriesBurned = 0
    for data in userData :
        totalWalked += data[0]
        totalSleep += data[3]
        totalJog += data[2]
        totalCaloriesBurned += data[7]




    return render_template("statistics.html",bmi = round(bmi,2),bmiStatement = bmiStatement, userData = userData,
    totalWalked = totalWalked,BMR = round(BMR,2), totalSleep = totalSleep, totalJog = totalJog, currentweight = rows[0][3]
    ,currentheight = rows[0][4], age = age, idealWeight = idealWeight, totalCaloriesBurned = totalCaloriesBurned)

@app.route("/diet_plans")
@login_required
def diet_plans():
    return render_template("diet_plans.html")

@app.route("/gym_nearby")
@login_required
def gym_nearby():

    return redirect("https://www.google.co.in/maps/search/GYM?hl=en&source=opensearch.html",code = 302)

@app.route("/yoga")
@login_required
def yoga():
    return render_template("yoga.html")

@app.route("/addDetails", methods = ["GET", "POST"])
@login_required
def addDetails():

    if request.method == "GET":
        return render_template("addDetails.html")

    elif request.method == "POST":
        username = session["user"]

        caloriesburn = int((0.42 * int(request.form.get("sleep"))) + (int(request.form.get("jog")) * 100) + (0.05 * int(request.form.get("steps"))))

        if (request.form.get("food") == "chicken"):
            caloriesburn += 199
        elif (request.form.get("food") == "naan"):
            caloriesburn += 137
        elif (request.form.get("food") == "palak paneer"):
            caloriesburn += 300
        elif (request.form.get("food") == "daal"):
            caloriesburn += 166

        db.execute("INSERT INTO dailyactivity (steps, food, jog, sleep, user, calories) VALUES (?,?,?,?,?,?)"
        ,(request.form.get("steps")
        ,request.form.get("food")
        ,request.form.get("jog")
        ,request.form.get("sleep")
        ,username
        ,caloriesburn))

        if request.form.get("weight")  :
            db.execute("UPDATE users SET weight = (?) WHERE username = (?)"
            ,(request.form.get("weight")
            ,username,))

        if request.form.get("height") :
            db.execute("UPDATE users SET height = (?) WHERE username = (?)"
            ,(request.form.get("height"), username,))
        return render_template("welcome.html")
        db.commit()

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
        usr = db.cursor()
        usr.execute("SELECT * FROM users WHERE username =?",(username,))
        rows = usr.fetchall()

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0][2]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0][0]

        session["user"] = request.form.get("username")
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
            return apology("all the feilds are neccessory!")
        elif request.form.get("password") != request.form.get("Re-password"):
            return apology("pasword do not match!")

        usr = db.cursor()
        usr.execute("SELECT username FROM users")
        rows = usr.fetchall()

        for data in rows:
            if data == request.form.get("username"):
                return apology("User already Registered")

        db.execute("INSERT INTO users (username, hash, age, gender, weight, height) VALUES(?,?,?,?,?,?)",
        (request.form.get("username"),
        pwd_context.hash(request.form.get("password")),
        request.form.get("age"),
        request.form.get("gender"),
        request.form.get("weight"),
        request.form.get("height"),))
        db.commit()
        return render_template("login.html")
    else:
        return render_template("register.html")



