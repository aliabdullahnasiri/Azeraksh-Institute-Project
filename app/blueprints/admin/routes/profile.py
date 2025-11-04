from flask import render_template
from flask_login import current_user, login_required

from app.forms.user import UpdateUserForm

from .. import bp


@bp.get("/profile")
@login_required
def profile():
    form = UpdateUserForm()

    return render_template(
        "admin/pages/profile.html",
        title="Profile",
        user=current_user,
        update_user_form=form,
    )
