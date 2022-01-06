from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import fresh_login_required, current_user
from .forms import UpdateAccountForm
from app.utils import save_picture
from app.models import User, Post
from app import db

users = Blueprint("users", __name__)


@users.route("/account", methods=["GET", "POST"])
@fresh_login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.avatar.data:
            avatar = save_picture(form.avatar.data)
            current_user.avatar = avatar
        current_user.email = form.email.data
        db.session.commit()
        flash("Account successfully updated")
        return redirect(url_for('users.account'))
    if request.method == "GET":
        form.email.data = current_user.email
    return render_template("account.html", form=form)


@users.route("/users/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author=user).order_by(Post.id.desc()).paginate(page=page, per_page=2)
    return render_template("user-posts.html", posts=posts, user=user)