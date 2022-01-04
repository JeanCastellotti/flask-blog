from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import RegistrationForm, LoginForm


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if True:
            flash("Votre compte a bien été créé", "success")
            return redirect(url_for("home"))
        else:
            flash("Vos identifiants sont incorrects", "error")
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # Check if method = post and validations
        flash("Vous êtes connecté", "success")
        return redirect(url_for("home"))
    return render_template("login.html", form=form)
