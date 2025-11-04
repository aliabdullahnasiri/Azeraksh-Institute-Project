import json
import re

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from sqlalchemy import and_
from wtforms import (
    DateField,
    DecimalField,
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

from app.models.phone import StudentPhone

from ..extensions import db
from ..models.job import Job
from ..models.student import Student


class AddStudentForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(max=50)])
    middle_name = StringField("Middle Name", validators=[Length(max=50)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(max=50)])
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(message="Enter a valid email address")],
    )
    birthday = DateField("Birthday", format="%Y-%m-%d", validators=[Optional()])
    avatar = FileField(
        "Upload new profile picture",
        validators=[FileAllowed(["jpg", "jpeg", "png"], "Images only!")],
    )
    phones = StringField("Phone", validators=[Optional()])
    submit = SubmitField("Add")

    # Check if email already exists
    def validate_email(self, email):
        if Student.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered")

    def validate_phones(self, phones):
        nums = json.loads(phones.data)

        for num in nums:
            if (
                db.session.query(StudentPhone)
                .filter(
                    StudentPhone.phone_number == num,
                )
                .first()
            ):

                raise ValidationError(f"Duplicate entry {num!r} for phone number!")

    def validate_job_id(self, job_id) -> None:
        pattern: re.Pattern = re.compile(r"^\d{0,}$")

        if not pattern.search(job_id.data):
            raise ValidationError("Not a valid decimal value.")
        elif not Job.query.filter_by(job_id=int(job_id.data)).first():
            raise ValidationError("Job with the given ID was not found :(")


class UpdateStudentForm(AddStudentForm):
    student_id = HiddenField("Student ID", validators=[DataRequired()])
    files = MultipleFileField(
        "Files",
        validators=[],
    )
    submit = SubmitField("Update")

    # Check if email already exists
    def validate_email(self, email):
        if (
            db.session.query(Student)
            .filter(
                and_(
                    Student.student_id != self.student_id.data,
                    Student.email == email.data,
                )
            )
            .first()
        ):
            raise ValidationError("Email already registered")

    def validate_phones(self, phones):
        nums = json.loads(phones.data)

        if hasattr(self, "student_id"):
            student_id = self.student_id.data

            for num in nums:
                if (
                    db.session.query(StudentPhone)
                    .filter(
                        and_(
                            StudentPhone.student_id != student_id,
                            StudentPhone.phone_number == num,
                        )
                    )
                    .first()
                ):

                    raise ValidationError(f"Duplicate entry {num!r} for phone number!")
