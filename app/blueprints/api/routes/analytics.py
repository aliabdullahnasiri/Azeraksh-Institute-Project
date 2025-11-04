import json
from datetime import datetime, timedelta, timezone

from flask import Response, jsonify
from flask_login import login_required
from sqlalchemy import extract, func

from app.blueprints.api import bp
from app.extensions import console, db
from app.models.payment import Payment
from app.models.student import Student
from app.models.view import View


@bp.get("/analytics/weekly-views")
@login_required
def weekly_views() -> Response:
    response: Response = Response(headers={"Content-Type": "application/json"})

    today = datetime.now().date()
    week_ago = today - timedelta(days=6)

    results = (
        db.session.query(
            func.date(View.created_at).label("date"), func.count(View.id).label("views")
        )
        .filter(View.created_at >= week_ago)
        .group_by(func.date(View.created_at))
        .order_by(func.date(View.created_at))
        .all()
    )

    x = []
    y = []

    for i in range(7):
        day = week_ago + timedelta(days=i)
        day_str = day.strftime("%a")

        count = next((r.views for r in results if r.date == day), 0)

        x.append(day_str)
        y.append(count)

    response.response = json.dumps(dict(zip(x, y)))
    response.status_code = 200

    return response


@bp.route("/analytics/monthly_students")
def monthly_students() -> Response:
    now = datetime.now()

    start_date = now.replace(day=1) - timedelta(days=360)

    results = (
        db.session.query(
            extract("year", Student.created_at).label("year"),
            extract("month", Student.created_at).label("month"),
            func.count(Student.student_id).label("count"),
        )
        .filter(Student.created_at >= start_date)
        .group_by("year", "month")
        .order_by("year", "month")
        .all()
    )

    # Prepare data
    x = []
    y = []

    for row in results:
        month_label = datetime(int(row.year), int(row.month), 1).strftime("%b")
        x.append(month_label)
        y.append(row.count)

    response: Response = Response(headers={"Content-Type": "application/json"})

    response.response = json.dumps(dict(zip(x, y)))

    return response


@bp.route("/analytics/monthly_payments")
def monthly_payments() -> Response:
    now = datetime.now(timezone.utc)
    start_date = now.replace(day=1) - timedelta(days=360)

    # Query: sum payments per month
    results = (
        db.session.query(
            extract("year", Payment.created_at).label("year"),
            extract("month", Payment.created_at).label("month"),
            func.sum(Payment.amount).label("total"),
        )
        .filter(Payment.created_at >= start_date)
        .group_by("year", "month")
        .order_by("year", "month")
        .all()
    )

    x = []
    y = []
    for row in results:
        month_label = datetime(int(row.year), int(row.month), 1).strftime("%b")
        x.append(month_label)
        y.append(f"{row.total:.2f}")

    response: Response = Response(headers={"Content-Type": "application/json"})
    response.response = json.dumps(dict(zip(x, y)))
    response.status_code = 200

    return response
