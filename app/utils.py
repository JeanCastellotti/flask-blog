import os
import secrets
from datetime import datetime, timedelta
from urllib.parse import urlparse, urljoin
from flask import request, url_for, current_app as app
from flask_mail import Message
from PIL import Image
from jose import jwt
from app.models import User
from app import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    file_name, file_ext = os.path.splitext(form_picture.filename)
    picture = random_hex + file_ext
    path = os.path.join(app.root_path, 'static', picture)
    output_size = (150, 150)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(path)
    return picture


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def create_jwt_token(user_id, minutes=30):
    payload = {"sub": str(user_id)}
    expiration = datetime.utcnow() + timedelta(minutes=minutes)
    payload.update({"exp": expiration})
    jwt_token = jwt.encode(payload, app.config["SECRET_KEY"])
    return jwt_token


def verify_jwt_token(token):
    try:
        payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms="HS256")
        user_id = payload.get("sub")
    except:
        return None
    return User.query.get(int(user_id))


def send_reset_email(user: User):
    token = create_jwt_token(user.id)
    message = Message("Password Reset Request", sender="noreply@demo.com", recipients=[user.email])
    message.body = f"To reset your password, visit the following link: {url_for('reset_password', token=token, _external=True)}"
    mail.send(message)