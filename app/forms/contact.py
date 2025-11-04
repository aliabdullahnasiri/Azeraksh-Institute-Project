from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


class ContactForm(FlaskForm):
    name = StringField("Your Name", validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField("Your Email", validators=[DataRequired(), Email()])
    subject = StringField(
        "Subject", validators=[DataRequired(), Length(min=5, max=100)]
    )
    message = TextAreaField(
        "Message", validators=[DataRequired(), Length(min=10, max=255)]
    )

    submit = SubmitField("Send Message")
