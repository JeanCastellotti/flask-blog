from flask import Blueprint, request, render_template
from app.models import Post

main = Blueprint("main", __name__)


@main.route("/")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.id.desc()).paginate(page=page, per_page=2)
    return render_template("home.html", posts=posts)