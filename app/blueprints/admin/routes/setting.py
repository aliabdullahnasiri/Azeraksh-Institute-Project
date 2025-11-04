from typing import Set, Union

from flask import render_template

from app.blueprints.admin import bp
from app.models.setting import Setting

from ....forms.setting import SettingForm


@bp.get("/settings")
def settings() -> str:
    setting: Union[Setting, None] = Setting.query.first()
    form: SettingForm = SettingForm(obj=setting)

    return render_template(
        "admin/pages/settings.html", title="Settings", setting=setting, form=form
    )
