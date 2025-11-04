import json
from collections import OrderedDict
from typing import Dict, List, Tuple, Union

from flask import Response
from flask_login import login_required

from app.blueprints.api import bp
from app.extensions import db
from app.forms import AddJobForm, UpdateJobForm
from app.models.job import Job
from app.types import ColumnID, ColumnName


@bp.get("/fetch/jobs")
@login_required
def fetch_jobs() -> Response:
    jobs: List[Dict] = [job.to_dict() for job in Job.query.all()]

    response: Response = Response(
        json.dumps(jobs),
        status=200,
        headers={"Content-Type": "application/json"},
    )

    return response


@bp.get("/fetch/rows/jobs")
@login_required
def fetch_jobs_rows() -> Response:
    response: Response = Response(
        headers={"Content-Type": "application/json"},
    )

    cols: List[Tuple[ColumnID, ColumnName]] = [
        (ColumnID("job_id"), ColumnName("Job ID")),
        (ColumnID("job_title"), ColumnName("Job Title")),
        (ColumnID("min_salary"), ColumnName("Min Salary")),
        (ColumnID("max_salary"), ColumnName("Max Salary")),
    ]

    jobs: List[Job] = Job.query.all()
    rows: List[List] = []

    for job in jobs:
        row: List = []

        for col_id, _ in cols:
            val = getattr(job, col_id)

            match col_id:
                case "min_salary":
                    row.append(job.display_min_salary)

                case "max_salary":
                    row.append(job.display_max_salary)

                case _:
                    row.append(val)

        rows.append(row)

    dct: Dict = {
        "cols": cols,
        "rows": rows,
    }

    response.response = json.dumps(dct)
    response.status_code = 200

    return response


@bp.get("/fetch/row/job/<int:job_id>")
@login_required
def fetch_job_row(job_id) -> Response:
    response: Response = Response()
    job: Union[Job, None] = Job.query.filter_by(job_id=job_id).first()

    if job:
        dct = OrderedDict(
            {
                "job_id": job.job_id,
                "job_title": job.job_title,
                "job_description": job.job_description,
                "min_salary": job.display_min_salary,
                "max_salary": job.display_max_salary,
            }
        )

        response.response = json.dumps(dct)
        response.status_code = 200
    else:
        dct = {
            "message": "Job with the given ID was not found :(",
            "category": "error",
        }
        response.response = json.dumps(dct)
        response.status_code = 404

    return response


@bp.get("/fetch/job/<int:job_id>")
@login_required
def fetch_job(job_id) -> Response:
    job: Union[Job, None] = Job.query.filter_by(job_id=job_id).first()

    if job:
        response: Response = Response(
            json.dumps(OrderedDict(job.to_dict())),
            status=200,
            headers={"Content-Type": "application/json"},
        )

        return response

    dct: Dict = {
        "message": "Job with the given ID was not found :(",
        "category": "error",
    }

    return Response(json.dumps(dct), status=404)


@bp.post("/update/job")
@login_required
def update_job() -> Response:
    form = UpdateJobForm()

    response: Dict = {}

    if form.validate_on_submit():
        job = Job.query.filter_by(job_id=form.job_id.data).first()

        if job:
            job.job_title = form.job_title.data
            job.job_description = form.job_description.data
            job.min_salary = form.min_salary.data
            job.max_salary = form.max_salary.data

            db.session.commit()

            response["title"] = "Good job!"
            response["category"] = "success"
            response["message"] = "Job updated successfully!"

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response), headers={"Content-Type": "application/json"}, status=200
    )


@bp.delete("/delete/job/<int:job_id>")
@login_required
def delete_job(job_id) -> Response:
    response: Dict = {}

    if job := Job.query.filter_by(job_id=job_id).first():
        db.session.delete(job)
        db.session.commit()

        response["title"] = "Deleted!"
        response["message"] = "Job deleted successfully"
        response["category"] = "success"
        response["status"] = 200

    else:
        response["title"] = "Error :("
        response["message"] = "Job with the given ID was not found :("
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )


@bp.post("/job/add")
@login_required
def add_job() -> Response:
    form = AddJobForm()

    response: Dict = {}

    if form.validate_on_submit():
        job = Job()

        job.job_title = form.job_title.data
        job.job_description = form.job_description.data
        job.min_salary = form.min_salary.data
        job.max_salary = form.max_salary.data

        db.session.add(job)
        db.session.commit()

        response["message"] = "Job added successfully"
        response["category"] = "success"
        response["title"] = "Job Added"
        response["id"] = job.job_id

    else:
        response["errors"] = form.errors

    return Response(json.dumps(response))
