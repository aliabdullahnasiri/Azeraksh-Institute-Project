import json
import pathlib
from typing import Dict, List, OrderedDict, Tuple, Union

from flask import Response, request
from flask_login import login_required
from sqlalchemy import and_

from app.extensions import db
from app.forms.course import AddCourseForm, UpdateCourseForm
from app.models.course import Course
from app.models.file import CourseFile, File
from app.types import ColumnID, ColumnName

from .. import bp


@bp.get("/fetch/courses")
@login_required
def fetch_courses() -> Response:
    courses: List[Course] = Course.query.all()

    response: Response = Response(
        json.dumps([c.to_dict() for c in courses]),
        status=200,
        headers={"Content-Type": "application/json"},
    )

    return response


@bp.get("/fetch/rows/courses")
@login_required
def fetch_courses_rows() -> Response:
    response: Response = Response(
        headers={"Content-Type": "application/json"},
    )

    cols: List[Tuple[ColumnID, ColumnName]] = [
        (ColumnID("course_id"), ColumnName("Course ID")),
        (ColumnID("course_title"), ColumnName("Title")),
        (ColumnID("start_date"), ColumnName("Start Date")),
        (ColumnID("end_date"), ColumnName("End Date")),
        (ColumnID("start_time"), ColumnName("Start Time")),
        (ColumnID("end_time"), ColumnName("End Time")),
        (ColumnID("monthly_fee"), ColumnName("Monthly Fee")),
    ]

    courses: List[Course] = Course.query.all()
    rows: List[List] = []

    for course in courses:
        row: List = []

        for col_id, _ in cols:
            match col_id:
                case "start_date":
                    row.append(course.display_start_date)
                case "end_date":
                    row.append(course.display_end_date)
                case "start_time":
                    row.append(course.display_start_time)
                case "end_time":
                    row.append(course.display_end_time)
                case "monthly_fee":
                    row.append(course.display_monthly_fee)
                case _:
                    row.append(getattr(course, col_id))

        rows.append(row)

    dct: Dict = {"cols": cols, "rows": rows}

    response.response = json.dumps(dct)
    response.status_code = 200

    return response


@bp.get("/fetch/course/<int:course_id>")
@login_required
def fetch_course(course_id: int) -> Response:
    course: Union[Course, None] = Course.query.filter_by(course_id=course_id).first()

    if course:
        response: Response = Response(
            json.dumps(OrderedDict(course.to_dict())),
            headers={"Content-Type": "application/json"},
            status=200,
        )
        return response

    return Response(
        json.dumps(
            {
                "message": "Course with the given ID was not found :(",
                "category": "error",
            }
        ),
        headers={"Content-Type": "application/json"},
        status=404,
    )


@bp.get("/fetch/row/course/<int:course_id>")
@login_required
def fetch_course_row(course_id: int) -> Response:
    response: Response = Response(headers={"Content-Type": "application/json"})
    course: Union[Course, None] = Course.query.filter_by(course_id=course_id).first()

    if course:
        dct = OrderedDict(
            {
                "course_id": course.course_id,
                "course_title": course.course_title,
                "start_date": course.display_start_date,
                "end_date": course.display_end_date,
                "start_time": course.display_start_time,
                "end_time": course.display_end_time,
                "monthly_fee": course.display_monthly_fee,
            }
        )

        response.response = json.dumps(dct)
        response.status_code = 200
    else:
        dct = {
            "message": "Course with the given ID was not found :(",
            "category": "error",
        }
        response.response = json.dumps(dct)
        response.status_code = 404

    return response


@bp.post("/update/course")
@login_required
def update_course() -> Response:
    form: UpdateCourseForm = UpdateCourseForm()
    response: Response = Response(headers={"Content-Type": "application/json"})

    if form.validate_on_submit():
        course: Union[Course, None] = Course.query.filter_by(
            course_id=form.course_id.data
        ).first()

        if course:

            course.course_title = form.course_title.data
            course.course_description = form.course_description.data
            course.teacher_id = form.teacher_id.data
            course.start_date = form.start_date.data
            course.end_date = form.end_date.data
            course.start_time = form.start_time.data
            course.end_time = form.end_time.data
            course.monthly_fee = form.monthly_fee.data

            try:
                links = request.form["links"]
                links = json.loads(links)

                if hasattr(links, "items"):
                    for name, links in links.items():
                        match name:
                            case "banner":
                                if links:
                                    link = links.pop()

                                    for f in course.files:
                                        if f.file.file_for == name:
                                            if f.file.file_url != link:
                                                db.session.delete(f)
                                                db.session.delete(f.file)

                                    else:
                                        db.session.commit()

                                        if not File.query.filter_by(
                                            file_url=link
                                        ).first():
                                            path: pathlib.Path = pathlib.Path(link)

                                            file: File = File()

                                            file.file_name = path.name
                                            file.file_url = f"{path!s}"
                                            file.file_for = name

                                            db.session.add(file)
                                            db.session.commit()

                                            course_file: CourseFile = CourseFile()
                                            course_file.file_id = file.file_id
                                            course_file.course_id = course.course_id

                                            db.session.add(course_file)
                                            db.session.commit()

                                else:
                                    for f in course.files:
                                        if f.file.file_for == name:
                                            db.session.delete(f)
                                            db.session.delete(f.file)

            except Exception as e:
                print(e)

            db.session.commit()

            response.response = json.dumps(
                {
                    "title": "Good job!",
                    "message": "Course updated successfully!",
                    "category": "success",
                }
            )
        else:
            pass
    else:
        response.response = json.dumps({"errors": form.errors})

    return response


@bp.delete("/delete/course/<int:course_id>")
@login_required
def delete_course(course_id: int) -> Response:
    course: Union[Course, None] = Course.query.filter_by(course_id=course_id).first()
    response: Response = Response()

    if course:
        db.session.delete(course)
        db.session.commit()

        dct = {
            "message": "Course deleted successfully",
            "category": "success",
            "status": 200,
        }

        response.response = json.dumps(dct)
        response.status_code = 200

    else:
        dct = {
            "message": "Course with the given ID was not found :(",
            "category": "error",
            "status": 404,
        }

        response.response = json.dumps(dct)
        response.status_code = 404

    return response


@bp.post("/add/course")
@login_required
def add_course() -> Response:
    form: AddCourseForm = AddCourseForm()
    response: Response = Response(headers={"Content-Type": "application/json"})

    if form.validate_on_submit():
        course: Course = Course()

        course.course_title = form.course_title.data
        course.course_description = form.course_description.data
        course.teacher_id = form.teacher_id.data
        course.start_date = form.start_date.data
        course.end_date = form.end_date.data
        course.start_time = form.start_time.data
        course.end_time = form.end_time.data
        course.monthly_fee = form.monthly_fee.data

        db.session.add(course)
        db.session.commit()

        try:
            links = request.form["links"]
            links = json.loads(links)

            if hasattr(links, "items"):
                for name, links in links.items():
                    match name:
                        case "banner":
                            link = links.pop()
                            path: pathlib.Path = pathlib.Path(link)

                            file: File = File()

                            file.file_name = path.name
                            file.file_url = f"{path!s}"
                            file.file_for = name

                            db.session.add(file)
                            db.session.commit()

                            course_file: CourseFile = CourseFile()
                            course_file.file_id = file.file_id
                            course_file.course_id = course.course_id

                            db.session.add(course_file)
                            db.session.commit()

        except Exception as e:
            print(e)

        dct = {}

        dct["message"] = "Course added successfully."
        dct["title"] = "Added!"
        dct["category"] = "success"
        dct["id"] = course.course_id

        response.response = json.dumps(dct)
    else:
        dct = {"errors": form.errors}

        response.response = json.dumps(dct)

    return response
