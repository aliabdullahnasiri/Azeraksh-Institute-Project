from flask import render_template
from flask_login import login_required

from app.forms.course import AddCourseForm, UpdateCourseForm

from .. import bp


@bp.get("/courses")
@login_required
def courses() -> str:
    add_course_form: AddCourseForm = AddCourseForm()
    update_course_form: UpdateCourseForm = UpdateCourseForm()

    return render_template(
        "admin/pages/courses.html",
        title="Courses",
        update_course_form=update_course_form,
        add_course_form=add_course_form,
    )
