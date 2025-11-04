from flask import render_template
from flask_login import login_required

from app.forms import AddEnrollmentForm, UpdateEnrollmentForm

from .. import bp


@bp.get("/enrollments")
@login_required
def enrollments():
    add_enrollment_form: AddEnrollmentForm = AddEnrollmentForm()
    update_enrollment_form: UpdateEnrollmentForm = UpdateEnrollmentForm()
    return render_template(
        "admin/pages/enrollments.html",
        title="Enrollments",
        add_enrollment_form=add_enrollment_form,
        update_enrollment_form=update_enrollment_form,
    )
