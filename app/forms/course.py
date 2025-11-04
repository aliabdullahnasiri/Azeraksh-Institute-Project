import re

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import (
    DateField,
    DecimalField,
    FileField,
    HiddenField,
    StringField,
    SubmitField,
    TextAreaField,
    TimeField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, NumberRange, Optional

from app.models.teacher import Teacher


class AddCourseForm(FlaskForm):
    course_title = StringField(
        "Course Title", validators=[DataRequired(), Length(max=255)]
    )
    teacher_id = StringField("Teacher ID", validators=[DataRequired()])

    course_description = TextAreaField(
        "Course Description", validators=[Optional(), Length(max=2000)]
    )

    start_date = DateField("Start Date", validators=[DataRequired()])
    end_date = DateField("End Date", validators=[DataRequired()])
    start_time = TimeField("Start Time", validators=[DataRequired()])
    end_time = TimeField("End Time", validators=[DataRequired()])
    monthly_fee = DecimalField(
        "Monthly Fee",
        places=2,
        validators=[DataRequired(), NumberRange(min=0)],
    )

    banner = FileField(
        "Upload the course banner",
        validators=[FileAllowed(["jpg", "jpeg", "png"], "Images only!")],
    )

    def validate_teacher_id(self, teacher_id) -> None:
        pattern: re.Pattern = re.compile(r"^\d{0,}$")

        if not pattern.search(teacher_id.data):
            raise ValidationError("Not a valid decimal value.")
        elif not Teacher.query.filter_by(teacher_id=int(teacher_id.data)).first():
            raise ValidationError("Teacher with the given ID was not found :(")

    submit = SubmitField("Add")


class UpdateCourseForm(AddCourseForm):
    course_id = HiddenField("Course ID", validators=[DataRequired()])

    submit = SubmitField("Update")
