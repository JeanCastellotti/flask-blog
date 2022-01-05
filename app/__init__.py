from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
# login_manager.session_protection = "strong"
login_manager.login_view = "login"
# login_manager.login_message = "Vous devez vous connecter"
# login_manager.login_message_category = "error"
login_manager.refresh_view = "reauthenticate"

from app import routes


# db.drop_all()
# db.create_all()
