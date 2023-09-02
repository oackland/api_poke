from flask import flash, redirect, url_for, request
from flask import render_template
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash

from ...models import User, db, InitialData
from . import auth
from .forms import LoginForm, SignupForm


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)

            initial_data = InitialData.query.filter_by(user_id=queried_user.id).first()
            if initial_data and initial_data.team:
                flash(f"Welcome back {queried_user.first_name}!", "primary")
                return redirect(url_for("main.game"))
            else:
                flash("Please complete the questionnaire to proceed", "info")
                return redirect(url_for("pokemon.questionnaire"))
        else:
            flash("Invalid email or password", "danger")
            return redirect(url_for("main.home"))
    else:
        return render_template("login.html", form=form)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if request.method == "POST" and form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data.lower()
        password = form.password.data
        new_user = User(first_name, last_name, email, password)

        db.session.add(new_user)
        db.session.commit()
        flash(f"Thank you for been a user {new_user.first_name}!", "primary")
        return redirect(url_for("auth.login"))

    else:
        return render_template("signup.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return render_template("index.html")


@auth.route("/check_team_value", methods=["GET"])
def check_team_value():
    initial_data = InitialData.query.filter_by(user_id=current_user.id).first()

    if initial_data and initial_data.team:
        return render_template("home.html")
    else:
        return render_template("questionnaire.html")
