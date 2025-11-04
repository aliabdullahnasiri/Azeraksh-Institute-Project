import re

from flask_wtf import FlaskForm
from wtforms import (
    DecimalField,
    HiddenField,
    MonthField,
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, Regexp

from app.models.enrollment import Enrollment


class AddPaymentForm(FlaskForm):
    enrollment_id = StringField(
        "Enrollment ID",
        validators=[DataRequired()],
    )
    amount = DecimalField("Amount", places=2, validators=[DataRequired()])
    month_for = MonthField("Month For", validators=[DataRequired()])
    submit = SubmitField("Add")

    def validate_enrollment_id(self, enrollment_id):
        pattern: re.Pattern = re.compile(r"^\d{0,}$")

        if not pattern.search(enrollment_id.data):
            raise ValidationError("Not a valid decimal value.")
        elif not Enrollment.query.filter_by(
            enrollment_id=int(enrollment_id.data)
        ).first():
            raise ValidationError("Enrollment with the given ID was not found :(")


class UpdatePaymentForm(AddPaymentForm):
    payment_id = HiddenField("Payment ID", validators=[DataRequired()])

    submit = SubmitField("Update")
