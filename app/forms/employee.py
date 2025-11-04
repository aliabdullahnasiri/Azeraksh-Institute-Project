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

from app.models.phone import EmployeePhone

from ..extensions import db
from ..models.employee import Employee
from ..models.job import Job


class AddEmployeeForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(max=50)])
    middle_name = StringField("Middle Name", validators=[Length(max=50)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(max=50)])
    email = StringField(
        "Email",
        validators=[Optional(), Email(message="Enter a valid email address")],
    )
    birthday = DateField("Birthday", format="%Y-%m-%d", validators=[Optional()])
    address = StringField("Address", validators=[Length(max=255)])
    salary = DecimalField(
        "Salary", places=2, validators=[Optional(), NumberRange(min=0)]
    )
    hire_date = DateField("Hire Date", format="%Y-%m-%d")
    job_id = StringField("Job ID", validators=[Optional()])
    avatar = FileField(
        "Upload new profile picture",
        validators=[FileAllowed(["jpg", "jpeg", "png"], "Images only!")],
    )
    phones = StringField("Phone", validators=[Optional()])
    submit = SubmitField("Add")

    # Check if email already exists
    def validate_email(self, email):
        if Employee.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered")

    def validate_phones(self, phones):
        nums = json.loads(phones.data)

        for num in nums:
            if (
                db.session.query(EmployeePhone)
                .filter(
                    EmployeePhone.phone_number == num,
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


class UpdateEmployeeForm(AddEmployeeForm):
    employee_id = HiddenField("Employee ID", validators=[DataRequired()])
    submit = SubmitField("Update")

    # Check if email already exists
    def validate_email(self, email):
        if (
            db.session.query(Employee)
            .filter(
                and_(
                    Employee.employee_id != self.employee_id.data,
                    Employee.email == email.data,
                )
            )
            .first()
        ):
            raise ValidationError("Email already registered")

    def validate_phones(self, phones):
        nums = json.loads(phones.data)

        if hasattr(self, "employee_id"):
            employee_id = self.employee_id.data

            for num in nums:
                if (
                    db.session.query(EmployeePhone)
                    .filter(
                        and_(
                            EmployeePhone.employee_id != employee_id,
                            EmployeePhone.phone_number == num,
                        )
                    )
                    .first()
                ):

                    raise ValidationError(f"Duplicate entry {num!r} for phone number!")
