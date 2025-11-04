from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import URL, DataRequired, Email, Optional


class SettingForm(FlaskForm):
    site_name = StringField("Site Name", validators=[DataRequired()])
    site_description = TextAreaField("Description", validators=[Optional()])
    location = StringField("Location", validators=[Optional()])
    primary_phone = StringField("Primary Phone", validators=[Optional()])
    email = StringField("Email", validators=[Optional(), Email()])

    facebook = StringField("Facebook", validators=[Optional(), URL()])
    twitter = StringField("Twitter", validators=[Optional(), URL()])
    instagram = StringField("Instagram", validators=[Optional(), URL()])
    linkedin = StringField("LinkedIn", validators=[Optional(), URL()])
    youtube = StringField("YouTube", validators=[Optional(), URL()])

    submit = SubmitField("Save Changes")
