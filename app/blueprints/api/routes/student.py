import json
import pathlib
from typing import Dict, List, OrderedDict, Tuple, Union

from flask import Response, current_app, request, url_for
from flask_login import login_required

from app.extensions import console, db
from app.forms.student import AddStudentForm, UpdateStudentForm
from app.models.file import File, StudentFile
from app.models.phone import StudentPhone
from app.models.student import Student
from app.types import ColumnID, ColumnName

from .. import bp


@bp.get("/fetch/students")
@login_required
def fetch_students() -> Response:
    students: List[Student] = Student.query.all()

    response: Response = Response(
        json.dumps([student.to_dict() for student in students]),
        status=200,
        headers={"Content-Type": "application/json"},
    )

    return response


@bp.get("/fetch/rows/students")
@login_required
def fetch_students_rows() -> Response:
    response: Response = Response(headers={"Content-Type": "application/json"})

    cols: List[Tuple[ColumnID, ColumnName]] = [
        (ColumnID("student_id"), ColumnName("Student ID")),
        (ColumnID("first_name"), ColumnName("First Name")),
        (ColumnID("middle_name"), ColumnName("Middle Name")),
        (ColumnID("last_name"), ColumnName("Last Name")),
        (ColumnID("email"), ColumnName("Email")),
        (ColumnID("birthday"), ColumnName("Birthday")),
    ]

    students: List[Student] = Student.query.all()
    rows: List[List] = []

    for student in students:
        row: List = []

        for col_id, _ in cols:
            val = getattr(student, col_id)

            match col_id:
                case "birthday":
                    row.append(student.display_birthday)
                case _:
                    row.append(val)

        rows.append(row)

    dct: Dict = {"cols": cols, "rows": rows}

    response.response = json.dumps(dct)
    response.status_code = 200
    return response


@bp.get("/fetch/student/<int:student_id>")
@login_required
def fetch_student(student_id: int) -> Response:
    student: Union[Student, None] = Student.query.filter_by(
        student_id=student_id
    ).first()

    if student:
        response: Response = Response(
            json.dumps(OrderedDict(student.to_dict())),
            headers={"Content-Type": "application/json"},
            status=200,
        )
        return response

    return Response(
        json.dumps(
            {
                "message": "Student with the given ID was not found :(",
                "category": "error",
            }
        ),
        headers={"Content-Type": "application/json"},
        status=404,
    )


@bp.get("/fetch/row/student/<int:student_id>")
@login_required
def fetch_student_row(student_id: int) -> Response:
    """Return a simplified row for a single student."""
    response: Response = Response()
    student: Union[Student, None] = Student.query.filter_by(
        student_id=student_id
    ).first()

    if student:
        dct = OrderedDict(
            {
                "student_id": student.student_id,
                "first_name": student.first_name,
                "middle_name": student.middle_name,
                "last_name": student.last_name,
                "email": student.email,
                "birthday": student.display_birthday,
            }
        )

        response.response = json.dumps(dct)
        response.status_code = 200
    else:
        dct = {
            "message": "Student with the given ID was not found :(",
            "category": "error",
        }
        response.response = json.dumps(dct)
        response.status_code = 404

    return response


@bp.post("/update/student")
@login_required
def update_student() -> Response:
    form: UpdateStudentForm = UpdateStudentForm()
    response: Response = Response(headers={"Content-Type": "application/json"})

    if form.validate_on_submit():
        student: Union[Student, None] = Student.query.filter_by(
            student_id=form.student_id.data
        ).first()

        if student:
            student.first_name = form.first_name.data
            student.middle_name = form.middle_name.data
            student.last_name = form.last_name.data
            student.email = form.email.data
            student.birthday = form.birthday.data

            if form.phones.data:
                nphones = json.loads(form.phones.data)
                ophones = student.phones

                for ophone in ophones:
                    if ophone.phone_number not in nphones:
                        db.session.delete(ophone)

                for nphone in nphones:
                    if (
                        not db.session.query(StudentPhone)
                        .filter(StudentPhone.phone_number == nphone)
                        .first()
                    ):
                        phone = StudentPhone()
                        phone.student_id = form.student_id.data
                        phone.phone_number = nphone

                        db.session.add(phone)
            else:
                for phone in student.phones:
                    db.session.delete(phone)

            try:
                links = request.form["links"]
                links = json.loads(links)

                if hasattr(links, "items"):
                    for name, link in links.items():
                        match name:
                            case "avatar":
                                student.avatar_path = link

                            case "files":
                                st: set = set(link)

                                for f in [f for f in student.files]:
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

                                    files.append(file)
                                    db.session.add(file)

                                db.session.commit()

                                for f in files:
                                    tf: StudentFile = StudentFile()

                                    tf.student_id = student.student_id
                                    tf.file_id = f.file_id

                                    db.session.add(tf)

                                if not len(st):
                                    for f in student.files:
                                        if f.file.file_for == name:
                                            db.session.delete(f.file)
                                            db.session.delete(f)

                                db.session.commit()

            except Exception as err:
                console.print(err)

            db.session.commit()

            response.response = json.dumps(
                {
                    "title": "Good job!",
                    "message": "Student updated successfully!",
                    "category": "success",
                }
            )
        else:
            pass
    else:
        response.response = json.dumps({"errors": form.errors})

    return response


@bp.delete("/delete/student/<int:student_id>")
@login_required
def delete_student(student_id: int) -> Response:
    student: Union[Student, None] = Student.query.filter_by(
        student_id=student_id
    ).first()
    response: Response = Response()

    if student:

        db.session.delete(student)
        db.session.commit()

        dct = {
            "message": "Student deleted successfully",
            "category": "success",
            "status": 200,
        }

        response.response = json.dumps(dct)
        response.status_code = 200

    else:
        dct = {
            "message": "Student with the given ID was not found :(",
            "category": "error",
            "status": 404,
        }

        response.response = json.dumps(dct)
        response.status_code = 404

    return response


@bp.post("/add/student")
@login_required
def add_student() -> Response:
    form: AddStudentForm = AddStudentForm()
    response: Response = Response(headers={"Content-Type": "application/json"})

    if form.validate_on_submit():
        student: Student = Student()

        student.first_name = form.first_name.data
        student.middle_name = form.middle_name.data
        student.last_name = form.last_name.data
        student.email = form.email.data
        student.birthday = form.birthday.data
        student.avatar_path = url_for(
            "static", filename=current_app.config["DEFAULT_AVATAR"]
        )

        db.session.add(student)
        db.session.commit()

        try:
            links = request.form["links"]
            links = json.loads(links)

            if hasattr(links, "items"):
                for name, link in links.items():
                    match name:
                        case "avatar":
                            student.avatar_path = link

        except Exception as e:
            print(e)

        if form.phones.data:
            for phone in json.loads(form.phones.data):
                student_phone = StudentPhone()
                student_phone.student_id = student.student_id
                student_phone.phone_number = phone

                db.session.add(student_phone)

            db.session.commit()

        dct = {}

        dct["message"] = "Student added successfully."
        dct["title"] = "Added!"
        dct["category"] = "success"
        dct["id"] = student.student_id

        response.response = json.dumps(dct)
    else:
        dct = {"errors": form.errors}

        response.response = json.dumps(dct)

    return response
