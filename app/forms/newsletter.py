from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class NewsletterForm(FlaskForm):
    email = StringField("Your Email", validators=[DataRequired(), Email()])

    submit = SubmitField("Sign Up")
