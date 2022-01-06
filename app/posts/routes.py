from flask import Blueprint, redirect, url_for, flash, render_template, abort, request
from flask_login import login_required, current_user
from app.models import Post
from app import db
from .forms import PostForm

posts = Blueprint("posts", __name__)

@posts.route("/posts/new", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Votre article a été publié", "success")
        return redirect(url_for("main.home"))
    return render_template("post-form.html", form=form)


@posts.route("/posts/<int:id>")
def get_post(id):
    post = Post.query.get_or_404(id)
    return render_template("post.html", post=post)


@posts.route("/posts/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        return abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated", "success")
        return redirect(url_for("posts.get_post", id=post.id))
    if request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("post-form.html", form=form)


@posts.route("/posts/<int:id>/delete", methods=["POST"])
def delete_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        return abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted successfully")
    return redirect(url_for("main.home"))