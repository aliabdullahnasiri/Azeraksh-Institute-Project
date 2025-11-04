import json
from typing import Dict, List, OrderedDict, Tuple, Union

from flask import Response, current_app, request, url_for
from flask_login import login_required

from app.blueprints.api import bp
from app.extensions import console, db
from app.forms import AddEmployeeForm
from app.forms.employee import UpdateEmployeeForm
from app.models.employee import Employee
from app.models.phone import EmployeePhone
from app.types import ColumnID, ColumnName


@bp.get("/fetch/employees")
@login_required
def fetch_employees() -> Response:
    employees: List[Employee] = Employee.query.all()

    response: Response = Response(
        json.dumps([employee.to_dict() for employee in employees]),
        status=200,
        headers={"Content-Type": "application/json"},
    )

    return response


@bp.get("/fetch/rows/employees")
@login_required
def fetch_employees_rows() -> Response:
    response: Response = Response(
        headers={"Content-Type": "application/json"},
    )

    cols: List[Tuple[ColumnID, ColumnName]] = [
        (ColumnID("employee_id"), ColumnName("Employee ID")),
        (ColumnID("first_name"), ColumnName("First Name")),
        (ColumnID("middle_name"), ColumnName("Middle Name")),
        (ColumnID("last_name"), ColumnName("Last Name")),
        (ColumnID("email"), ColumnName("Email")),
        (ColumnID("hire_date"), ColumnName("Hire Date")),
    ]

    jobs: List[Employee] = Employee.query.all()
    rows: List[List] = []

    for job in jobs:
        row: List = []

        for col_id, _ in cols:
            val = getattr(job, col_id)

            match col_id:
                case "hire_date":
                    row.append(job.display_hire_date)

                case _:
                    row.append(val)

        rows.append(row)

    dct: Dict = {
        "cols": cols,
        "rows": rows,
    }

    response.response = json.dumps(dct)
    response.status_code = 200

    return response


@bp.get("/fetch/employee/<int:employee_id>")
@login_required
def fetch_employee(employee_id) -> Response:
    employee: Union[Employee, None] = Employee.query.filter_by(
        employee_id=employee_id
    ).first()

    if employee:
        response: Response = Response(
            json.dumps(OrderedDict(employee.to_dict())),
            headers={"Content-Type": "application/json"},
            status=200,
        )
        return response

    return Response(
        json.dumps(
            {
                "message": "Employee with the given ID was not found :(",
                "category": "error",
            }
        ),
        headers={"Content-Type": "application/json"},
        status=404,
    )


@bp.get("/fetch/row/employee/<int:employee_id>")
@login_required
def fetch_employee_row(employee_id) -> Response:
    response: Response = Response()
    employee: Union[Employee, None] = Employee.query.filter_by(
        employee_id=employee_id
    ).first()

    if employee:
        dct = OrderedDict(
            {
                "employee_id": employee.employee_id,
                "first_name": employee.first_name,
                "middle_name": employee.middle_name,
                "last_name": employee.last_name,
                "email": employee.email,
                "hire_date": employee.display_hire_date,
            }
        )

        response.response = json.dumps(dct)
        response.status_code = 200
    else:
        dct = {
            "message": "Employee with the given ID was not found :(",
            "category": "error",
        }
        response.response = json.dumps(dct)
        response.status_code = 404

    return response


@bp.post("/update/employee")
@login_required
def update_employee() -> Response:
    form: UpdateEmployeeForm = UpdateEmployeeForm()

    response: Response = Response(headers={"Content-Type": "application/json"})

    if form.validate_on_submit():
        employee: Union[Employee, None] = Employee.query.filter_by(
            employee_id=form.employee_id.data
        ).first()

        if employee:
            employee.first_name = form.first_name.data
            employee.middle_name = form.middle_name.data
            employee.last_name = form.last_name.data
            employee.email = form.email.data
            employee.birthday = form.birthday.data
            employee.address = form.address.data
            employee.salary = form.salary.data

            if form.job_id.data:
                employee.job_id = form.job_id.data

            db.session.commit()

            try:
                links = json.loads(request.form.get("links", "{}"))

                if type(links) == dict:
                    for key, value in links.items():
                        match key:
                            case "avatar":
                                if value:
                                    employee.avatar_path = value

            except Exception as err:
                console.print(err)

            if form.phones.data:
                try:
                    nphones = json.loads(form.phones.data)
                    ophones = employee.phones

                    for ophone in ophones:
                        if ophone.phone_number not in nphones:
                            db.session.delete(ophone)

                    for nphone in nphones:
                        if (
                            not db.session.query(EmployeePhone)
                            .filter(EmployeePhone.phone_number == nphone)
                            .first()
                        ):
                            phone = EmployeePhone()
                            phone.employee_id = form.employee_id.data
                            phone.phone_number = nphone

                            db.session.add(phone)

                    db.session.commit()
                except Exception as err:
                    console.print(err)

            else:
                for phone in employee.phones:
                    db.session.delete(phone)

                db.session.commit()

            response.response = json.dumps(
                {
                    "title": "Good job!",
                    "message": "Employee updated successfully!",
                    "category": "success",
                }
            )

    else:
        response.response = json.dumps({"errors": form.errors})

    return response


@bp.delete("/delete/employee/<int:employee_id>")
@login_required
def delete_employee(employee_id) -> Response:
    employee: Union[Employee, None] = Employee.query.filter_by(
        employee_id=employee_id
    ).first()

    response: Response = Response(headers={"Content-Type": "application/json"})

    if employee:
        db.session.delete(employee)
        db.session.commit()

        response.response = json.dumps(
            {
                "title": "Deleted!",
                "message": "Employee deleted successfully",
                "category": "success",
                "status": 200,
            }
        )

        response.status_code = 200

    else:
        response.response = json.dumps(
            {
                "title": "Error :(",
                "message": "Employee with the given ID was not found :(",
                "category": "error",
                "status": 404,
            }
        )
        response.status_code = 404

    return response


@bp.post("/add/employee")
@login_required
def add_employee() -> Response:
    form: AddEmployeeForm = AddEmployeeForm()

    response: Dict = {}

    if form.validate_on_submit():
        employee: Employee = Employee()

        employee.first_name = form.first_name.data
        employee.middle_name = form.middle_name.data
        employee.last_name = form.last_name.data
        if form.email.data:
            employee.email = form.email.data
        employee.birthday = form.birthday.data
        employee.address = form.address.data
        employee.salary = form.salary.data
        if form.job_id.data:
            employee.job_id = form.job_id.data
        employee.avatar_path = url_for(
            "static", filename=current_app.config["DEFAULT_AVATAR"]
        )

        try:
            links = json.loads(request.form.get("links", "{}"))

            if type(links) == dict:
                for key, value in links.items():
                    match key:
                        case "avatar":
                            if value:
                                employee.avatar_path = value

        except Exception as err:
            console.print(err)

        db.session.add(employee)
        db.session.commit()

        if form.phones.data:
            try:
                for phone in json.loads(form.phones.data):
                    if EmployeePhone.query.filter_by(phone_number=phone).first():
                        continue

                    employee_phone = EmployeePhone()
                    employee_phone.employee_id = employee.employee_id
                    employee_phone.phone_number = phone

                    db.session.add(employee_phone)

                db.session.commit()
            except Exception as err:
                console.print(err)

        response["message"] = "Employee added successfully."
        response["title"] = "Added!"
        response["category"] = "success"
        response["id"] = employee.employee_id

    else:
        response["errors"] = form.errors

    return Response(json.dumps(response), status=200)
