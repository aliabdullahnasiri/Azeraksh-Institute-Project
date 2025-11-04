from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = EmailField(
        "Email",
        validators=[DataRequired(), Email(message="Enter a valid email address")],
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")
