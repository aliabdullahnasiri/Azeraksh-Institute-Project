import re
from decimal import Decimal

from flask_wtf import FlaskForm
from sqlalchemy import and_
from wtforms import (
    DecimalField,
    HiddenField,
    SelectField,
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Regexp

from app.models.course import Course
from app.models.enrollment import Enrollment, EnrollmentStatus
from app.models.student import Student


class AddEnrollmentForm(FlaskForm):
    course_id = StringField(
        "Course ID",
        validators=[
            DataRequired(),
            Length(max=255),
            Regexp(re.compile(r"^\d{0,}$"), message="Not a valid decimal value."),
        ],
    )
    student_id = StringField(
        "Student ID",
        validators=[
            DataRequired(),
            Regexp(re.compile(r"^\d{0,}$"), message="Not a valid decimal value."),
        ],
    )
    discount_rate = StringField(
        "Discount Rate",
        validators=[
            Optional(),
            Regexp(
                re.compile(r"^\d*\.?\d+%?$"),
                message="Oops! The percentage format looks wrong. Try something like 10.00%.",
            ),
        ],
        default="00.00%",
    )
    status = SelectField(
        "Status",
        validators=[DataRequired()],
        choices=[
            EnrollmentStatus.ACTIVE.value,
            EnrollmentStatus.CLOSED.value,
        ],
        default=EnrollmentStatus.ACTIVE.value,
    )

    def validate_discount_rate(self, discount_rate):
        pattern: re.Pattern = re.compile(r"(\d*\.?\d+)%?")

        match = re.search(pattern, discount_rate.data)

        if match:
            value = float(match.group(1))

            if 0 <= value <= 100:
                discount_rate.data = value
            else:
                raise ValidationError("Percentage must be between 0 and 100.")

    def validate_course_id(self, course_id) -> None:
        if Enrollment.query.filter_by(
            student_id=self.student_id.data, course_id=course_id.data
        ).first():
            raise ValidationError("Each student can only enroll in a course once.")
        elif not Course.query.filter_by(course_id=int(course_id.data)).first():
            raise ValidationError("Course with the given ID was not found :(")

    def validate_student_id(self, student_id) -> None:
        if not Student.query.filter_by(student_id=int(student_id.data)).first():
            raise ValidationError("Student with the given ID was not found :(")

    submit = SubmitField("Add")


class UpdateEnrollmentForm(AddEnrollmentForm):
    enrollment_id = HiddenField("Enrollment ID", validators=[DataRequired()])

    submit = SubmitField("Update")

    def validate_course_id(self, course_id) -> None:
        if Enrollment.query.filter(
            and_(
                Enrollment.enrollment_id != self.enrollment_id.data,
                Enrollment.course_id == course_id.data,
                Enrollment.student_id == self.student_id.data,
            )
        ).first():
            raise ValidationError("Each student can only enroll in a course once.")
        elif not Course.query.filter_by(course_id=int(course_id.data)).first():
            raise ValidationError("Course with the given ID was not found :(")
