from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Nom d'utilisateur", validators=[DataRequired(), Length(min=4, max=12)])
    email = EmailField("Email", validators=[DataRequired(), Email("Adresse email invalide")])
    password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField("Confirmation mot de passe", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Créer mon compte")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Le nom d'utilisateur est déjà pris")

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError("Cette adresse email est déjà prise")


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    remember = BooleanField("Se souvenir de moi")
    submit = SubmitField("Se connecter")

class ReauthenticateLogin(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Se connecter")

class CreatePostForm(FlaskForm):
    title = StringField("Titre")
    content = TextAreaField("Contenu")
    submit = SubmitField("Envoyer")