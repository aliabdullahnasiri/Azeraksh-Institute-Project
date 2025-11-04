from typing import Union

from flask import render_template

from app.blueprints.admin import bp
from app.models import Enrollment


@bp.get("/view/enrollment/<int:enrollment_id>")
def view_enrollment(enrollment_id) -> str:
    enrollment: Union[Enrollment, None] = Enrollment.query.filter_by(
        enrollment_id=enrollment_id
    ).first()

    if enrollment:
        return render_template("admin/views/enrollment.html", enrollment=enrollment)

    return str()
