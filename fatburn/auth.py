from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import db, User
from .helpers import apology

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register user."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        re_password = request.form.get("Re-password")

        if not username or not password or not re_password:
            return apology("all the fields are necessary!")
        if password != re_password:
            return apology("passwords do not match!")

        # Check if user exists
        stmt = db.select(User).where(User.username == username)
        user = db.session.execute(stmt).scalar_one_or_none()

        if user:
            return apology("User already Registered")

        try:
            age = int(request.form.get("age"))
            weight = float(request.form.get("weight"))
            height = float(request.form.get("height"))
            gender = request.form.get("gender")
        except (ValueError, TypeError):
             return apology("Invalid input for age, weight or height")

        new_user = User(
            username=username,
            age=age,
            gender=gender,
            weight=weight,
            height=height
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    else:
        return render_template("register.html")

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in."""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("must provide username")
        elif not password:
            return apology("must provide password")

        stmt = db.select(User).where(User.username == username)
        user = db.session.execute(stmt).scalar_one_or_none()

        if user is None or not user.check_password(password):
            return apology("invalid username and/or password")

        session["user_id"] = user.id
        session["user"] = user.username

        return redirect(url_for("main.index"))

    else:
        return render_template("login.html")

@bp.route('/logout')
def logout():
    """Log user out."""
    session.clear()
    return redirect(url_for("auth.login"))
