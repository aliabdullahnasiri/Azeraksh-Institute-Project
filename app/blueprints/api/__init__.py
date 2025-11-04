from flask import Blueprint, redirect, url_for
from flask_login import current_user

from app.models.user import Role

bp = Blueprint("api", __name__)


@bp.before_request
def _():
    if current_user.role != Role.ADMIN:
        return redirect(url_for("auth.login"))


from .routes import (
    analytics,
    course,
    employee,
    enrollment,
    job,
    main,
    payment,
    setting,
    student,
    teacher,
    upload,
    user,
)
