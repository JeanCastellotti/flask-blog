from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField(
        "Nom d'utilisateur",
        validators=[
            DataRequired("Le nom d'utilisateur est obligatoire"),
            Length(
                min=4,
                max=12,
                message="Le nom d'utilisateur doit faire entre 4 et 12 caractères",
            ),
        ],
    )
    email = EmailField(
        "Email",
        validators=[
            DataRequired("L'adresse email est obligatoire"),
            Email("Adresse email invalide"),
        ],
    )
    password = PasswordField(
        "Mot de passe",
        validators=[
            DataRequired("Le mot de passe est obligatoire"),
            Length(min=8, message="Le mot de passe doit faire au moins 8 caractères"),
        ],
    )
    password_confirm = PasswordField(
        "Confirmation mot de passe",
        validators=[
            DataRequired("Veuillez confirmer le mot de passe"),
            EqualTo("password", message="Les mots de passe ne correspondent pas"),
        ],
    )
    submit = SubmitField("Créer mon compte")


class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[
            DataRequired("L'adresse email est obligatoire"),
            Email("L'adresse email n'est pas valide"),
        ],
    )
    password = PasswordField(
        "Mot de passe", validators=[DataRequired("Le mot de passe est obligatoire")]
    )
    remember = BooleanField("Se souvenir de moi")
    submit = SubmitField("Se connecter")
