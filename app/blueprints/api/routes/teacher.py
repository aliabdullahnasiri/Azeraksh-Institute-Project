import json
import pathlib
from typing import Dict, List, Tuple, Union

from flask import Response, current_app, request, url_for
from flask_login import login_required

from app.blueprints.api import bp
from app.extensions import console, db
from app.forms.teacher import AddTeacherForm, UpdateTeacherForm
from app.models.file import File, TeacherFile
from app.models.phone import TeacherPhone
from app.models.teacher import Teacher
from app.types import ColumnID, ColumnName


@bp.get("/fetch/teachers")
@login_required
def fetch_teachers() -> Response:
    teachers: List[Teacher] = Teacher.query.all()

    response: Response = Response(headers={"Content-Type": "application/json"})

    rows: List[Dict] = []

    for teacher in teachers:
        dct = teacher.to_dict()
        rows.append(dct)

    response.response = json.dumps(rows)
    response.status_code = 200

    return response


@bp.get("/fetch/rows/teachers")
@login_required
def fetch_teachers_rows():
    teachers: List[Teacher] = Teacher.query.all()
    response: Response = Response(headers={"Content-Type": "application/json"})

    cols: List[Tuple[ColumnID, ColumnName]] = [
        (ColumnID("teacher_id"), ColumnName("Teacher ID")),
        (ColumnID("first_name"), ColumnName("First Name")),
        (ColumnID("middle_name"), ColumnName("Middle Name")),
        (ColumnID("last_name"), ColumnName("Last Name")),
        (ColumnID("email"), ColumnName("Email")),
        (ColumnID("birthday"), ColumnName("Birthday")),
    ]
    rows: List[List] = []

    for teacher in teachers:
        row = []

        for col_id, _ in cols:
            val = getattr(teacher, col_id)

            match col_id:
                case col if col == "birthday":
                    row.append(teacher.display_birthday)

                case col if col == "salary":
                    row.append(teacher.display_salary)

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


@bp.get("/fetch/teacher/<int:teacher_id>")
@login_required
def fetch_teacher(teacher_id: int) -> Response:
    teacher: Union[Teacher, None] = Teacher.query.filter_by(
        teacher_id=teacher_id
    ).first()

    response: Response = Response(headers={"Content-Type": "application/json"})

    if teacher:
        response.response = json.dumps(teacher.to_dict())
        response.status_code = 200
    else:
        dct = {
            "message": "Teacher with the given ID was not found :(",
            "category": "error",
        }

        response.response = json.dumps(dct)
        response.status_code = 404

    return response


@bp.get("/fetch/row/teacher/<int:teacher_id>")
@login_required
def fetch_teacher_row(teacher_id) -> Response:
    teacher: Union[Teacher, None] = Teacher.query.filter_by(
        teacher_id=teacher_id
    ).first()

    response: Response = Response(headers={"Content-Type": "application/json"})

    if teacher:
        dct = {
            "teacher_id": teacher.teacher_id,
            "first_name": teacher.first_name,
            "middle_name": teacher.middle_name,
            "last_name": teacher.last_name,
            "email": teacher.email,
            "birthday": teacher.display_birthday,
        }

        response.response = json.dumps(dct)
        response.status_code = 200
    else:
        dct = {
            "message": "Teacher with the given ID was not found :(",
            "category": "error",
            "status": 404,
        }

        response.response = json.dumps(dct)
        response.status_code = 404

    return response


@bp.post("/update/teacher")
@login_required
def update_teacher() -> Response:
    form: UpdateTeacherForm = UpdateTeacherForm()
    response: Response = Response(headers={"Content-Type": "application/json"})

    if form.validate_on_submit():
        teacher: Union[Teacher, None] = Teacher.query.filter_by(
            teacher_id=form.teacher_id.data
        ).first()

        if teacher:
            teacher.first_name = form.first_name.data
            teacher.middle_name = form.middle_name.data
            teacher.last_name = form.last_name.data
            teacher.email = form.email.data
            teacher.birthday = form.birthday.data
            teacher.salary = form.salary.data

            db.session.commit()

            if form.phones.data:
                nphones = json.loads(form.phones.data)
                ophones = teacher.phones

                for ophone in ophones:
                    if ophone.phone_number not in nphones:
                        db.session.delete(ophone)

                for nphone in nphones:
                    if (
                        not db.session.query(TeacherPhone)
                        .filter(TeacherPhone.phone_number == nphone)
                        .first()
                    ):
                        phone = TeacherPhone()
                        phone.teacher_id = form.teacher_id.data
                        phone.phone_number = nphone

                        db.session.add(phone)

                db.session.commit()
            else:
                for phone in teacher.phones:
                    db.session.delete(phone)

            try:
                links = request.form["links"]
                links = json.loads(links)

                if hasattr(links, "items"):
                    for name, link in links.items():
                        match name:
                            case "avatar":
                                teacher.avatar_path = link

                            case "resume":
                                st: set = set(link)

                                for f in [
                                    f
                                    for f in teacher.files
                                    if f.file.file_for == "resume"
                                ]:
                                    if f.file.file_url not in st:
                                        db.session.delete(f)
                                        db.session.delete(f.file)

                                db.session.commit()

                                files: List[File] = []
                                for l in st:
                                    if File.query.filter_by(file_url=l).first():
                                        continue

                                    path: pathlib.Path = pathlib.Path(l)
                                    file: File = File()
                                    file.file_name = path.name
                                    file.file_url = path
                                    file.file_for = "resume"

                                    files.append(file)
                                    db.session.add(file)

                                db.session.commit()

                                for f in files:
                                    tf: TeacherFile = TeacherFile()

                                    tf.teacher_id = teacher.teacher_id
                                    tf.file_id = f.file_id

                                    db.session.add(tf)

                                if not len(st):
                                    for f in teacher.files:
                                        if f.file.file_for == name:
                                            db.session.delete(f.file)
                                            db.session.delete(f)

                                db.session.commit()
            except Exception as err:
                console.print(err)

            response.response = json.dumps(
                {
                    "title": "Good job!",
                    "message": "Teacher updated successfully!",
                    "category": "success",
                }
            )
        else:
            pass
    else:
        response.response = json.dumps({"errors": form.errors})

    return response


@bp.delete("/delete/teacher/<int:teacher_id>")
@login_required
def delete_teacher(teacher_id) -> Response:
    teacher: Union[Teacher, None] = Teacher.query.filter_by(
        teacher_id=teacher_id
    ).first()
    response: Response = Response()

    if teacher:
        db.session.delete(teacher)
        db.session.commit()

        dct = {
            "message": "Teacher deleted successfully",
            "category": "success",
            "status": 200,
        }

        response.response = json.dumps(dct)
        response.status_code = 200

    else:
        dct = {
            "message": "Teacher with the given ID was not found :(",
            "category": "error",
            "status": 404,
        }

        response.response = json.dumps(dct)
        response.status_code = 404

    return response


@bp.post("/add/teacher")
@login_required
def add_teacher() -> Response:
    form: AddTeacherForm = AddTeacherForm()
    response: Response = Response(headers={"Content-Type": "application/json"})

    if form.validate_on_submit():
        teacher: Teacher = Teacher()

        teacher.first_name = form.first_name.data
        teacher.middle_name = form.middle_name.data
        teacher.last_name = form.last_name.data
        teacher.email = form.email.data
        teacher.birthday = form.birthday.data
        teacher.salary = form.salary.data
        teacher.avatar_path = url_for(
            "static", filename=current_app.config["DEFAULT_AVATAR"]
        )
        db.session.add(teacher)
        db.session.commit()

        try:
            links = request.form["links"]
            links = json.loads(links)

            if hasattr(links, "items"):
                for name, link in links.items():
                    match name:
                        case "avatar":
                            teacher.avatar_path = link

                        case "resume":
                            if type(link) == list:
                                files: List[File] = []

                                for l in link:
                                    if File.query.filter_by(file_url=l).first():
                                        continue

                                    path: pathlib.Path = pathlib.Path(l)

                                    file: File = File()

                                    file.file_name = path.name
                                    file.file_url = path
                                    file.file_for = name

                                    db.session.add(file)
                                    files.append(file)

                                db.session.commit()

                                for file in files:
                                    teacher_file: TeacherFile = TeacherFile()
                                    teacher_file.file_id = file.file_id
                                    teacher_file.teacher_id = teacher.teacher_id

                                    db.session.add(teacher_file)

                                db.session.commit()

        except Exception as e:
            print(e)

        if form.phones.data:
            for phone in json.loads(form.phones.data):
                teacher_phone = TeacherPhone()
                teacher_phone.teacher_id = teacher.teacher_id
                teacher_phone.phone_number = phone

                db.session.add(teacher_phone)

            db.session.commit()

        dct = {}

        dct["message"] = "Teacher added successfully."
        dct["title"] = "Added!"
        dct["category"] = "success"
        dct["id"] = teacher.teacher_id

        response.response = json.dumps(dct)
    else:
        dct = {"errors": form.errors}

        response.response = json.dumps(dct)

    return response
