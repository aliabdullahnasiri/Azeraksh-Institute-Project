from flask_wtf import FlaskForm
from wtforms import DecimalField, HiddenField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class UpdateJobForm(FlaskForm):
    job_id = HiddenField("Job ID", validators=[DataRequired()])

    job_title = StringField("Job Title", validators=[DataRequired(), Length(max=255)])

    job_description = TextAreaField(
        "Job Description", validators=[Optional(), Length(max=2000)]
    )

    min_salary = DecimalField(
        "Minimum Salary", places=2, validators=[DataRequired(), NumberRange(min=0)]
    )

    max_salary = DecimalField(
        "Maximum Salary", places=2, validators=[DataRequired(), NumberRange(min=0)]
    )

    submit = SubmitField("Update")


class AddJobForm(FlaskForm):
    job_title = StringField("Job Title", validators=[DataRequired(), Length(max=255)])

    job_description = TextAreaField(
        "Job Description", validators=[Optional(), Length(max=2000)]
    )

    min_salary = DecimalField(
        "Minimum Salary", places=2, validators=[DataRequired(), NumberRange(min=0)]
    )

    max_salary = DecimalField(
        "Maximum Salary", places=2, validators=[DataRequired(), NumberRange(min=0)]
    )

    submit = SubmitField("Add")
