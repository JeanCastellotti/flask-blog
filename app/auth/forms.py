from flask_wtf import FlaskForm
from wtforms.fields import StringField, EmailField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
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


class RequestPasswordResetForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Réinitialiser mon mot de passe")

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is None:
    #         raise ValidationError("There is no account with that email.")


class PasswordResetForm(FlaskForm):
    password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=8)])
    password_confirm = PasswordField("Confirmation mot de passe", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Réinitialiser mon mot de passe")