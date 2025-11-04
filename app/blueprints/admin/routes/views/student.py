from typing import Union

from flask import render_template

from .....models import Student
from ....admin import bp


@bp.get("/view/student/<int:student_id>")
def view_student(student_id: int) -> str:
    student: Union[Student, None] = Student.query.filter_by(
        student_id=student_id
    ).first()

    if student:
        return render_template("admin/views/student.html", student=student)

    return str()
