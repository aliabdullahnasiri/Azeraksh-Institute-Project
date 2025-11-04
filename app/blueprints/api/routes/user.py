import json
from typing import Dict, List, Tuple, Union

from flask import Response, request, url_for
from flask_login import login_required

from app.blueprints.api import bp
from app.constants import DEFAULT_AVATAR
from app.extensions import console, db
from app.forms import AddUserForm, UpdateUserForm
from app.models.user import User
from app.types import ColumnID, ColumnName


@bp.get("/fetch/users")
@login_required
def fetch_users() -> Response:
    users: List[User] = [user.to_dict() for user in User.query.all()]

    response: Response = Response(
        json.dumps(users), headers={"Content-Type": "application/json"}
    )
    response.status_code = 200

    return response


@bp.get("/fetch/rows/users")
@login_required
def fetch_users_rows() -> Response:
    users: List[User] = User.query.all()

    cols: List[Tuple[ColumnID, ColumnName]] = [
        (ColumnID("user_id"), ColumnName("User ID")),
        (ColumnID("first_name"), ColumnName("First Name")),
        (ColumnID("middle_name"), ColumnName("Middle Name")),
        (ColumnID("last_name"), ColumnName("Last Name")),
        (ColumnID("user_name"), ColumnName("User Name")),
        (ColumnID("email"), ColumnName("Email")),
        (ColumnID("birthday"), ColumnName("Birthday")),
    ]

    rows: List[List] = []

    for user in users:
        row: List = []
        dct: Dict = user.to_dict()

        for col_id, _ in cols:
            val = dct.get(col_id, "N/A")

            row.append(val)

        rows.append(row)

    dct: Dict = {
        "cols": cols,
        "rows": rows,
    }

    response: Response = Response(
        json.dumps(dct),
        status=200,
        headers={"Content-Type": "application/json"},
    )

    return response


@bp.get("/fetch/row/user/<int:user_id>")
@login_required
def fetch_user_row(user_id) -> Response:
    response: Response = Response()

    user: Union[User, None] = User.query.filter_by(user_id=user_id).first()

    if user:
        response.response = json.dumps(user.to_dict())
        response.status_code = 200

    else:
        dct = {
            "message": "User with the given ID was not found :(",
            "category": "error",
        }

        response.response = json.dumps(dct)
        response.status_code = 404

    return response


@bp.get("/fetch/user/<int:user_id>")
@login_required
def fetch_user(user_id) -> Response:
    user = User.query.filter_by(user_id=user_id).first()

    if user:
        response: Response = Response(
            json.dumps(user.to_dict()),
            status=200,
            headers={"Content-Type": "application/json"},
        )

        return response

    return Response(
        json.dumps(
            {
                "message": "User with the given ID was not found :(",
                "category": "error",
            }
        ),
        headers={"Content-Type": "application/json"},
        status=404,
    )


@bp.post("/update/user")
@login_required
def update_user() -> Response:
    form = UpdateUserForm()

    response: Dict = {}

    if form.validate_on_submit():
        user = User.query.filter_by(user_id=form.user_id.data).first()

        if user:
            user.first_name = form.first_name.data
            user.middle_name = form.middle_name.data
            user.last_name = form.last_name.data
            user.user_name = form.user_name.data
            user.email = form.email.data
            user.birthday = form.birthday.data

            try:
                links = request.form["links"]
                links = json.loads(links)

                if type(links) == dict:
                    for name, link in links.items():
                        match name:
                            case "avatar":
                                user.avatar_path = link

            except Exception as err:
                console.print(err)

            db.session.commit()

            response["title"] = "Good job!"
            response["category"] = "success"
            response["message"] = "User updated successfully!"

    else:
        response["errors"] = form.errors

    return Response(
        json.dumps(response), headers={"Content-Type": "application/json"}, status=200
    )


@bp.delete("/delete/user/<int:user_id>")
@login_required
def delete_user(user_id):
    response = {}

    if user := User.query.filter_by(user_id=user_id).first():
        db.session.delete(user)
        db.session.commit()

        response["title"] = "Deleted!"
        response["message"] = "User deleted successfully"
        response["category"] = "success"
        response["status"] = 200

    else:
        response["title"] = "Error :("
        response["message"] = "User not found"
        response["category"] = "error"
        response["status"] = 404

    return Response(
        json.dumps(response),
        status=response["status"],
        headers={"Content-Type": "application/json"},
    )


@bp.post("/add/user")
@login_required
def add_user() -> Response:
    form = AddUserForm()

    response: Dict = {}

    if form.validate_on_submit():
        user = User()

        user.first_name = form.first_name.data
        user.middle_name = form.middle_name.data
        user.last_name = form.last_name.data
        user.user_name = form.user_name.data
        user.email = form.email.data
        user.birthday = form.birthday.data
        user.avatar_path = url_for("static", filename=DEFAULT_AVATAR)

        try:
            links = request.form["links"]
            links = json.loads(links)

            if type(links) == dict:
                for name, link in links.items():
                    match name:
                        case "avatar":
                            user.avatar_path = link

        except Exception as err:
            console.print(err)

        if passwd := form.password.data:
            user.set_password(passwd)

        db.session.add(user)
        db.session.commit()

        response["message"] = "User added successfully"
        response["category"] = "success"
        response["title"] = "User Added"
        response["id"] = user.user_id

    else:
        response["errors"] = form.errors

    return Response(json.dumps(response))
