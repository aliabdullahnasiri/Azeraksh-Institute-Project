from typing import Union

from flask import render_template

from .....models import Teacher
from ....admin import bp


@bp.get("/view/teacher/<int:teacher_id>")
def view_teacher(teacher_id) -> str:
    teacher: Union[Teacher, None] = Teacher.query.filter_by(
        teacher_id=teacher_id
    ).first()

    if teacher:
        return render_template("admin/views/teacher.html", teacher=teacher)

    return str()
