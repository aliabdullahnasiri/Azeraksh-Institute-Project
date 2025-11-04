import json
from typing import Union

from flask import Response
from flask_login import login_required

from app.extensions import db
from app.forms.setting import SettingForm
from app.models.setting import Setting

from .. import bp


@bp.post("/update/setting")
@login_required
def update_setting() -> Response:
    response: Response = Response(headers={"Content-Type": "application/json"})
    setting: Union[Setting, None] = Setting.query.first()
    form = SettingForm()

    if form.validate_on_submit():
        if setting:
            setting.site_name = form.site_name.data
            setting.site_description = form.site_description.data
            setting.primary_phone = form.primary_phone.data
            setting.email = form.email.data
            setting.location = form.location.data

            setting.facebook = form.facebook.data
            setting.twitter = form.twitter.data
            setting.instagram = form.instagram.data
            setting.linkedin = form.linkedin.data
            setting.youtube = form.youtube.data

            db.session.commit()

            dct = {}
            dct["message"] = "Settings updated successfully."
            dct["title"] = "Updated!"
            dct["category"] = "success"
            dct["id"] = setting.id

            response.response = json.dumps(dct)

    else:
        response.response = json.dumps({"errors": form.errors})

    return response
