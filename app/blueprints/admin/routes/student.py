from flask import render_template
from flask_login import login_required

from app.forms.student import AddStudentForm, UpdateStudentForm

from .. import bp


@bp.get("/students")
@login_required
def students():
    add_student_form = AddStudentForm()
    update_student_form = UpdateStudentForm()

    return render_template(
        "admin/pages/students.html",
        title="Students",
        update_student_form=update_student_form,
        add_student_form=add_student_form,
    )
