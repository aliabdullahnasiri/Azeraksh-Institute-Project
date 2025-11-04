from flask import render_template
from flask_login import login_required

from app.forms.job import AddJobForm, UpdateJobForm

from .. import bp


@bp.get("/jobs")
@login_required
def jobs():
    update_job_form = UpdateJobForm()
    add_job_form = AddJobForm()

    return render_template(
        "admin/pages/jobs.html",
        title="Jobs",
        update_job_form=update_job_form,
        add_job_form=add_job_form,
    )
