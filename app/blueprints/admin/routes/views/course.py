from typing import Union

from flask import render_template

from .....models import Course
from ....admin import bp


@bp.get("/view/course/<int:course_id>")
def view_course(course_id) -> str:
    course: Union[Course, None] = Course.query.filter_by(course_id=course_id).first()

    if course:
        return render_template("admin/views/course.html", course=course)

    return str()
