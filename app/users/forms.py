from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms.fields import EmailField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from app.models import User

class UpdateAccountForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Update")
    avatar = FileField("Avatar", validators=[FileAllowed(["jpg", "jpeg", "png"])])

    def validate_email(self, email):
        if email.data == current_user.email: 
            return
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists")