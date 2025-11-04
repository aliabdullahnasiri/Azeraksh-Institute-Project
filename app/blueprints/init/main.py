import json
from typing import Union

from flask import Response, redirect, render_template, request, url_for

from app.blueprints.init import bp
from app.extensions import console, db
from app.forms.setting import SettingForm
from app.models.setting import Setting


@bp.before_request
def _():
    if Setting.query.first():
        return redirect(url_for("main.home"))


@bp.route("/setup", methods=["POST", "GET"])
def setup() -> Union[str, Response]:
    form: SettingForm = SettingForm()

    if request.method == "POST":
        response: Response = Response()

        if form.validate_on_submit():
            if not Setting.query.count():
                setting: Setting = Setting()
                form.populate_obj(setting)

                db.session.add(setting)
                db.session.commit()

                dct = {}

                dct["message"] = "Setting successfully saved!"
                dct["title"] = "Saved!"
                dct["category"] = "success"
                dct["id"] = setting.id
                dct["redirect"] = url_for("main.home")

                response.response = json.dumps(dct)

        else:
            response.response = json.dumps({"errors": form.errors})
            response.status_code = 400

        return response

    return render_template("init/setup.html", form=form)
