from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import db, User, DailyActivity
from .helpers import login_required

bp = Blueprint('main', __name__)

@bp.route("/")
@login_required
def index():
    return render_template("welcome.html")

@bp.route("/exercises")
@login_required
def exercises():
    return render_template("exercises.html")

@bp.route("/statistics")
@login_required
def statistics():
    user_id = session["user_id"]
    user = db.session.execute(db.select(User).where(User.id == user_id)).scalar_one()

    # Height is stored in inches, Weight in kg (assumed based on BMR formula which usually uses kg)
    # But wait, BMR formula used in original:
    # Male: 66.47 + (13.75 * weight) + (5.0 * height) - (6.75 * age)
    # This is Harris-Benedict. Weight in kg, Height in cm.
    # If height is in inches, 5.0 * height is wrong (should be height in cm).
    # Original code was: 5.0 * height.
    # If height is 70 inches (177 cm), 5 * 70 = 350. 5 * 177 = 885. Big difference.
    # I will convert height to cm for BMR calculation.

    height_in = user.height
    weight_kg = user.weight
    age = user.age

    height_m = height_in * 0.0254
    height_cm = height_in * 2.54

    bmi = weight_kg / (height_m ** 2) if height_m > 0 else 0

    if bmi <= 18.5:
        bmi_statement = 'which means you are underweight.'
    elif 18.5 < bmi < 25:
        bmi_statement = 'which means you are normal.'
    elif 25 <= bmi < 30:
        bmi_statement = 'overweight.'
    else:
        bmi_statement = 'which means you are obese.'

    if user.gender == "male":
        bmr = 66.47 + (13.75 * weight_kg) + (5.003 * height_cm) - (6.755 * age)
    else:
        bmr = 655.1 + (9.563 * weight_kg) + (1.850 * height_cm) - (4.676 * age)
        # Original used 665.09 ...

    ideal_weight = int(height_cm - 100) # Broca's index approx? Original was - 101.
    # Original: idealWeight = int(heightInCm - 101)

    activities = db.session.execute(
        db.select(DailyActivity).where(DailyActivity.user_id == user_id)
    ).scalars().all()

    total_walked = sum(a.steps for a in activities if a.steps)
    total_sleep = sum(a.sleep for a in activities if a.sleep)
    total_jog = sum(a.jog for a in activities if a.jog)
    total_calories_burned = sum(a.calories for a in activities if a.calories)

    return render_template("statistics.html",
                           bmi=round(bmi, 2),
                           bmiStatement=bmi_statement,
                           userData=activities,
                           totalWalked=total_walked,
                           BMR=round(bmr, 2),
                           totalSleep=total_sleep,
                           totalJog=total_jog,
                           currentweight=user.weight,
                           currentheight=user.height,
                           age=user.age,
                           idealWeight=ideal_weight,
                           totalCaloriesBurned=total_calories_burned)

@bp.route("/diet_plans")
@login_required
def diet_plans():
    return render_template("diet_plans.html")

@bp.route("/gym_nearby")
@login_required
def gym_nearby():
    return redirect("https://www.google.co.in/maps/search/GYM?hl=en&source=opensearch.html", code=302)

@bp.route("/yoga")
@login_required
def yoga():
    return render_template("yoga.html")

@bp.route("/addDetails", methods=["GET", "POST"])
@login_required
def addDetails():
    if request.method == "GET":
        return render_template("addDetails.html")
    elif request.method == "POST":
        user_id = session["user_id"]

        try:
            sleep = int(request.form.get("sleep") or 0)
            jog = int(request.form.get("jog") or 0)
            steps = int(request.form.get("steps") or 0)
            food = request.form.get("food")
        except ValueError:
             return render_template("addDetails.html", error="Invalid input")

        caloriesburn = int((0.42 * sleep) + (jog * 100) + (0.05 * steps))

        food_calories = {
            "chicken": 199,
            "naan": 137,
            "palak paneer": 300,
            "daal": 166
        }

        caloriesburn += food_calories.get(food, 0)

        activity = DailyActivity(
            steps=steps,
            food=food,
            jog=jog,
            sleep=sleep,
            user_id=user_id,
            calories=caloriesburn
        )
        db.session.add(activity)

        # Update user weight/height if provided
        user = db.session.execute(db.select(User).where(User.id == user_id)).scalar_one()
        if request.form.get("weight"):
            user.weight = float(request.form.get("weight"))
        if request.form.get("height"):
            user.height = float(request.form.get("height"))

        db.session.commit()
        return redirect(url_for("main.index"))
