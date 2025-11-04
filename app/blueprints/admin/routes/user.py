from flask import render_template
from flask_login import login_required

from app.forms.user import AddUserForm, UpdateUserForm

from .. import bp


@bp.get("/users")
@login_required
def users():
    update_user_form = UpdateUserForm()
    add_user_form = AddUserForm()

    return render_template(
        "admin/pages/users.html",
        title="Users",
        update_user_form=update_user_form,
        add_user_form=add_user_form,
    )
