from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from sqlalchemy import and_
from wtforms import (
    DateField,
    FileField,
    HiddenField,
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, Length, Optional, ValidationError

from app.extensions import db
from app.models.user import User


class AddUserForm(FlaskForm):
    first_name = StringField("First Name", validators=[Length(max=50)])
    middle_name = StringField("Middle Name", validators=[Length(max=50)])
    last_name = StringField("Last Name", validators=[Length(max=50)])
    user_name = StringField("Username", validators=[DataRequired(), Length(max=50)])
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Enter a valid email address")],
    )
    password = PasswordField("Password", validators=[DataRequired()])
    birthday = DateField("Birthday", format="%Y-%m-%d", validators=[Optional()])
    avatar = FileField(
        "Upload new profile picture",
        validators=[FileAllowed(["jpg", "jpeg", "png"], "Images only!")],
    )

    submit = SubmitField("Add")

    # Check if username already exists
    def validate_user_name(self, user_name):
        if User.query.filter_by(user_name=user_name.data).first():
            raise ValidationError("Username already taken")

    # Check if email already exists
    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered")


class UpdateUserForm(FlaskForm):
    user_id = HiddenField("User ID", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[Length(max=50)])
    middle_name = StringField("Middle Name", validators=[Length(max=50)])
    last_name = StringField("Last Name", validators=[Length(max=50)])
    user_name = StringField("User Name", validators=[DataRequired(), Length(max=50)])
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Enter a valid email address")],
    )
    birthday = DateField("Birthday", format="%Y-%m-%d", validators=[Optional()])

    avatar = FileField(
        "Upload new profile picture",
        validators=[FileAllowed(["jpg", "jpeg", "png"], "Images only!")],
    )
    submit = SubmitField("Update")

    # Check if username already exists
    def validate_user_name(self, user_name):
        if (
            db.session.query(User)
            .filter(
                and_(
                    User.user_id != self.user_id.data, User.user_name == user_name.data
                )
            )
            .first()
        ):
            raise ValidationError("Username already taken")
