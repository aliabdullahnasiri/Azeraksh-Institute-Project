from typing import Union

from flask import render_template

from .....models import Job
from ....admin import bp


@bp.get("/view/job/<int:job_id>")
def view_job(job_id) -> str:
    job: Union[Job, None] = Job.query.filter_by(job_id=job_id).first()

    if job:
        return render_template("admin/views/job.html", job=job)

    return str()
