from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from ..models.user import User


class SignupForm(FlaskForm):
    user_name = StringField("Username", validators=[DataRequired(), Length(max=50)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    submit = SubmitField("Sign Up")

    # Check if username already exists
    def validate_user_name(self, user_name):
        if User.query.filter_by(user_name=user_name.data).first():
            raise ValidationError("Username already taken")

    # Check if email already exists
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered")
