from typing import Union

from flask import render_template

from .....models import Employee
from ....admin import bp


@bp.get("/view/employee/<int:employee_id>")
def view_employee(employee_id) -> str:
    employee: Union[Employee, None] = Employee.query.filter_by(
        employee_id=employee_id
    ).first()

    if employee:
        return render_template("admin/views/employee.html", employee=employee)

    return str()
