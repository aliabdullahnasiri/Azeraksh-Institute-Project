from flask import render_template
from flask_login import login_required

from app.forms.employee import AddEmployeeForm, UpdateEmployeeForm

from .. import bp


@bp.get("/employees")
@login_required
def employees():
    add_employee_form = AddEmployeeForm()
    update_employee_form = UpdateEmployeeForm()

    return render_template(
        "admin/pages/employees.html",
        title="Employees",
        update_employee_form=update_employee_form,
        add_employee_form=add_employee_form,
    )
