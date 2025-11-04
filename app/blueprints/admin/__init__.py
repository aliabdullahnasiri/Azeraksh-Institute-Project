from flask import Blueprint, redirect, url_for
from flask_login import current_user

from app.models.user import Role

bp = Blueprint("admin", __name__)


@bp.before_request
def _():
    if current_user.role != Role.ADMIN:
        return redirect(url_for("auth.login"))


from .routes import (
    course,
    dashboard,
    employee,
    enrollment,
    job,
    payment,
    profile,
    setting,
    student,
    teacher,
    user,
)
from .routes.views import course, employee, enrollment, job, student, teacher
