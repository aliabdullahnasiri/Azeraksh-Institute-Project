from flask import render_template
from flask_login import login_required

from app.forms.teacher import AddTeacherForm, UpdateTeacherForm

from .. import bp


@bp.get("/teachers")
@login_required
def teachers() -> str:
    add_teacher_form: AddTeacherForm = AddTeacherForm()
    update_teacher_form: UpdateTeacherForm = UpdateTeacherForm()

    return render_template(
        "admin/pages/teachers.html",
        title="Teachers",
        add_teacher_form=add_teacher_form,
        update_teacher_form=update_teacher_form,
    )
