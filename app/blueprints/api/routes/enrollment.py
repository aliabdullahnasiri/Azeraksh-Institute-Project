import json
import math
from datetime import datetime
from typing import Dict, List, OrderedDict, Tuple, Union

from flask import Response, current_app, render_template
from flask_login import login_required

from app.extensions import db
from app.forms.enrollment import AddEnrollmentForm, UpdateEnrollmentForm
from app.models.enrollment import Enrollment, EnrollmentStatus
from app.types import ColumnID, ColumnName

from .. import bp


@bp.get("/fetch/enrollments")
@login_required
def fetch_enrollments() -> Response:
    """Return all enrollments as JSON (full dicts)."""
    enrollments: List[Enrollment] = Enrollment.query.all()

    response: Response = Response(
        json.dumps([e.to_dict() for e in enrollments]),
        status=200,
        headers={"Content-Type": "application/json"},
    )

    return response


@bp.get("/fetch/rows/enrollments")
@login_required
def fetch_enrollments_rows() -> Response:
    """Return all enrollments as rows for table display using ColumnID/ColumnName."""
    response: Response = Response(headers={"Content-Type": "application/json"})

    cols: List[Tuple[ColumnID, ColumnName]] = [
        (ColumnID("enrollment_id"), ColumnName("ID")),
        (ColumnID("student"), ColumnName("Student")),
        (ColumnID("status"), ColumnName("Status")),
        (ColumnID("enrollment_date"), ColumnName("Date")),
        (ColumnID("monthly_fee"), ColumnName("Monthly Fee")),
        (ColumnID("discount_rate"), ColumnName("Discount Rate")),
    ]

    enrollments: List[Enrollment] = Enrollment.query.all()
    rows: List[List] = []

    for e in enrollments:
        row: List = []

        for col_id, _ in cols:
            match col_id:
                case "student":
                    s = e.student
                    row.append(
                        render_template(
                            "admin/components/tables/td/student.html",
                            avatar_path=s.avatar_path,
                            full_name=f"{s.first_name} {s.middle_name or ''} {s.last_name}".strip(),
                            email=s.email,
                        )
                    )
                case "status":
                    c = "success" if e.status == EnrollmentStatus.ACTIVE else "danger"
                    row.append(
                        render_template(
                            "admin/components/tables/td/status.html",
                            value=e.status.value,
                            category=c,
                        )
                    )
                case "enrollment_date":
                    row.append(e.display_enrollment_date)
                case "monthly_fee":
                    row.append(e.display_monthly_fee)
                case "discount_rate":
                    row.append(e.display_discount_rate)
                case _:
                    row.append(getattr(e, col_id, "N/A"))

        rows.append(row)

    dct: Dict = {"cols": cols, "rows": rows}

    response.response = json.dumps(dct)
    response.status_code = 200

    return response


@bp.get("/fetch/enrollment/<int:enrollment_id>")
@login_required
def fetch_enrollment(enrollment_id: int) -> Response:
    response: Response = Response(
        headers={"Content-Type": "application/json"},
    )

    enrollment: Union[Enrollment, None] = Enrollment.query.filter_by(
        enrollment_id=enrollment_id
    ).first()

    if enrollment:
        response.response = json.dumps(OrderedDict(enrollment.to_dict()))
        response.status_code = 200
    else:
        dct = {
            "message": "Enrollment with the given ID was not found :(",
            "category": "error",
        }

        response.response = json.dumps(dct)
        response.status_code = 404

    return response


@bp.get("/fetch/row/enrollment/<int:enrollment_id>")
@login_required
def fetch_enrollment_row(enrollment_id: int) -> Response:
    enrollment: Union[Enrollment, None] = Enrollment.query.filter_by(
        enrollment_id=enrollment_id
    ).first()
    response: Response = Response(headers={"Content-Type": "application/json"})

    if enrollment:
        s = enrollment.student
        dct = OrderedDict(
            {
                "enrollment_id": enrollment.enrollment_id,
                "student": render_template(
                    "admin/components/tables/td/student.html",
                    avatar_path=s.avatar_path,
                    full_name=f"{s.first_name} {s.middle_name or ''} {s.last_name}".strip(),
                    email=s.email,
                ),
                "status": render_template(
                    "admin/components/tables/td/status.html",
                    value=enrollment.display_status,
                    category=(
                        "success"
                        if enrollment.status == EnrollmentStatus.ACTIVE
                        else "danger"
                    ),
                ),
                "enrollment_date": enrollment.display_enrollment_date,
                "monthly_fee": enrollment.display_monthly_fee,
                "discount_rate": enrollment.display_discount_rate,
            }
        )
        response.response = json.dumps(dct)
        response.status_code = 200
    else:
        response.response = json.dumps(
            {"message": "Enrollment not found", "category": "error"}
        )
        response.status_code = 404

    return response


@bp.post("/update/enrollmednt")
@login_required
def update_enrollment() -> Response:
    form: UpdateEnrollmentForm = UpdateEnrollmentForm()
    response: Response = Response(headers={"Content-Type": "application/json"})

    if form.validate_on_submit():
        enrollment: Union[Enrollment, None] = Enrollment.query.filter_by(
            enrollment_id=form.enrollment_id.data
        ).first()

        if enrollment:
            enrollment.student_id = form.student_id.data
            enrollment.course_id = form.course_id.data
            if form.discount_rate.data:
                enrollment.discount_rate = form.discount_rate.data

            if form.status.data:
                enrollment.status = form.status.data

            db.session.commit()

            response.response = json.dumps(
                {
                    "title": "Good job!",
                    "message": "Enrollment updated successfully!",
                    "category": "success",
                }
            )
        else:
            pass
    else:
        response.response = json.dumps({"errors": form.errors})

    return response


@bp.delete("/delete/enrollment/<int:enrollment_id>")
@login_required
def delete_enrollment(enrollment_id: int) -> Response:
    enrollment: Union[Enrollment, None] = Enrollment.query.filter_by(
        enrollment_id=enrollment_id
    ).first()
    response: Response = Response()

    if enrollment:
        db.session.delete(enrollment)
        db.session.commit()

        dct = {
            "message": "Enrollment deleted successfully",
            "category": "success",
            "status": 200,
        }

        response.response = json.dumps(dct)
        response.status_code = 200

    else:
        dct = {
            "message": "Enrollment with the given ID was not found :(",
            "category": "error",
            "status": 404,
        }

        response.response = json.dumps(dct)
        response.status_code = 404

    return response


@bp.post("/add/enrollment")
@login_required
def add_enrollment() -> Response:
    form: AddEnrollmentForm = AddEnrollmentForm()
    response: Response = Response(headers={"Content-Type": "application/json"})

    if form.validate_on_submit():
        enrollment: Enrollment = Enrollment()

        enrollment.student_id = form.student_id.data
        enrollment.course_id = form.course_id.data
        enrollment.enrollment_date = datetime.now().date().strftime("%Y-%m-%d")
        enrollment.discount_rate = (
            form.discount_rate.data if form.discount_rate.data else 0
        )
        enrollment.status = form.status.data

        db.session.add(enrollment)
        db.session.commit()

        dct = {}

        dct["message"] = "Enrollment added successfully."
        dct["title"] = "Added!"
        dct["category"] = "success"
        dct["id"] = enrollment.enrollment_id

        response.response = json.dumps(dct)
    else:
        dct = {"errors": form.errors}

        response.response = json.dumps(dct)

    return response
