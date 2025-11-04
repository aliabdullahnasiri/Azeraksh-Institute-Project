import json
import re

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from sqlalchemy import and_
from wtforms import (
    DateField,
    DecimalField,
    EmailField,
    FileField,
    HiddenField,
    MultipleFileField,
    StringField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    NumberRange,
    Optional,
    ValidationError,
)

from app.models.phone import TeacherPhone

from ..extensions import db
from ..models.teacher import Teacher


class AddTeacherForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(max=50)])
    middle_name = StringField("Middle Name", validators=[Optional(), Length(max=50)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(max=50)])

    email = EmailField(
        "Email", validators=[DataRequired(), Email("Enter a valid email address")]
    )

    birthday = DateField("Birthday", format="%Y-%m-%d", validators=[Optional()])
    salary = DecimalField(
        "Salary", places=2, validators=[Optional(), NumberRange(min=0)]
    )

    resume = MultipleFileField(
        "Resume",
        validators=[FileAllowed(["pdf"], "PDF only!")],
    )

    avatar = FileField(
        "Avatar",
        validators=[FileAllowed(["jpg", "jpeg", "png"], "Images only!")],
    )

    phones = StringField("Phone", validators=[Optional()])
    submit = SubmitField("Add")

    # Check if email already exists
    def validate_email(self, email):
        if Teacher.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered")

    def validate_phones(self, phones):
        nums = json.loads(phones.data)

        for num in nums:
            if (
                db.session.query(TeacherPhone)
                .filter(
                    TeacherPhone.phone_number == num,
                )
                .first()
            ):

                raise ValidationError(f"Duplicate entry {num!r} for phone number!")


class UpdateTeacherForm(AddTeacherForm):
    teacher_id = HiddenField("Teacher ID", validators=[DataRequired()])
    submit = SubmitField("Update")

    # Check if email already exists
    def validate_email(self, email):
        if (
            db.session.query(Teacher)
            .filter(
                and_(
                    Teacher.teacher_id != self.teacher_id.data,
                    Teacher.email == email.data,
                )
            )
            .first()
        ):
            raise ValidationError("Email already registered")

    def validate_phones(self, phones):

        nums = json.loads(phones.data)

        if hasattr(self, "employee_id"):
            teacher_id = self.teacher_id.data

            for num in nums:
                if (
                    db.session.query(TeacherPhone)
                    .filter(
                        and_(
                            TeacherPhone.teacher_id != teacher_id,
                            TeacherPhone.phone_number == num,
                        )
                    )
                    .first()
                ):

                    raise ValidationError(f"Duplicate entry {num!r} for phone number!")
