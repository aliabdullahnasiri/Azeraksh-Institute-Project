import json

from flask import render_template
from flask_login import login_required

from app.blueprints.admin import bp
from app.models.course import Course
from app.models.employee import Employee
from app.models.enrollment import Enrollment, EnrollmentStatus
from app.models.payment import Payment
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.user import User
from app.models.view import View


@bp.get("/")
@bp.get("/dashboard")
@login_required
def dashboard():
    return render_template("admin/pages/dashboard.html", title="Dashboard", **globals())
