from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from app.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
# login_manager.login_message = "Vous devez vous connecter"
# login_manager.login_message_category = "error"
login_manager.refresh_view = "reauthenticate"
migrate = Migrate()

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from .auth.routes import auth
    from .users.routes import users
    from .posts.routes import posts
    from .main.routes import main
    from .errors.handlers import errors

    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
