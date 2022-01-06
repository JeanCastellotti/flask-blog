from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import current_user, login_fresh, login_user, login_required, logout_user, confirm_login
from app import bcrypt, db
from app.models import User
from app.utils import is_safe_url, verify_jwt_token, send_reset_email
from .forms import RegistrationForm, LoginForm, LoginForm, RequestPasswordResetForm, PasswordResetForm

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            pass
        flash("Votre compte a bien été créé", "success")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Vous êtes connecté", "success")
            next = request.args.get("next")
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for("main.home"))
        flash("Vos identifiants sont incorrects")
    return render_template("login.html", form=form)


@auth.route("/reauthenticate", methods=["GET", "POST"])
def reauthenticate():
    if not current_user.is_authenticated or login_fresh():
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        emails_match = current_user.email == form.email.data
        passwords_match = bcrypt.check_password_hash(current_user.password, form.password.data)
        if emails_match and passwords_match:
            confirm_login()
            flash("Vous êtes connecté", "success")
            next = request.args.get("next")
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for("main.home"))
        flash("Vos identifiants sont incorrects")
    return render_template("reauthenticate.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))


@auth.route("/request-password", methods=["GET", "POST"])
def request_password():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user :
            send_reset_email(user)
        flash("An email has been sent with instructions to reset your password")
        return redirect(url_for("auth.login"))
    return render_template("request-password.html", form=form)


@auth.route("/reset-password/<string:token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = verify_jwt_token(token)
    if user is None:
        flash("Invalid or expired token", "warning")
        return redirect(url_for("auth.request_password"))
    form = PasswordResetForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been successfully updated")
        return redirect(url_for("auth.login"))
    return render_template("reset-password.html", form=form)
