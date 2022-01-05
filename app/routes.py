from flask import render_template, flash, redirect, url_for, request, abort, session
from flask_login import login_user, logout_user, current_user, login_required, fresh_login_required, confirm_login, login_fresh
from app import app, db, bcrypt
# from app import app
from app.forms import RegistrationForm, LoginForm, CreatePostForm
from app.models import User
from app.utils import is_safe_url


@app.route("/")
def home():
    print(session)
    return render_template("home.html")


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if current_user.is_authenticated: 
#         return redirect(url_for("home"))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
#         user = User(username=form.username.data, email=form.email.data, password=hashed_password)
#         try:
#             db.session.add(user)
#             db.session.commit()
#         except:
#             pass
#         flash("Votre compte a bien été créé", "success")
#         return redirect(url_for("login"))
#     return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated: 
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("Vous êtes connecté", "success")
            next = request.args.get("next")
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for("home"))
        flash("Vos identifiants sont incorrects")
    return render_template("login.html", form=form)


@app.route("/reauthenticate", methods=["GET", "POST"])
def reauthenticate():
    if not current_user.is_authenticated or login_fresh():
        return redirect(url_for("home"))
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
            return redirect(next or url_for("home"))
        flash("Vos identifiants sont incorrects")
    return render_template("reauthenticate.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/account")
@fresh_login_required
def account():
    return render_template("account.html")

@app.route("/create-post")
def create_post():
    form = CreatePostForm()
    return render_template("create-post.html", form=form)