from typing import List

from flask import Response, render_template

from app.forms.contact import ContactForm
from app.forms.newsletter import NewsletterForm
from app.forms.search import SearchForm
from app.models.course import Course
from app.models.student import Student
from app.models.teacher import Teacher

from . import bp


@bp.context_processor
def _():
    return {
        "Course": Course,
        "Student": Student,
        "Teacher": Teacher,
        "Form": {
            "Contact": ContactForm(),
            "Search": SearchForm(),
            "Newsletter": NewsletterForm(),
        },
    }


@bp.get("/")
def home() -> str:
    return render_template("main/pages/home.html", title="Home")


@bp.get("/about")
def about() -> str:
    return render_template("main/pages/about.html", title="About")


@bp.route("/contact", methods=["GET", "POST"])
def contact() -> str:
    return render_template("main/pages/contact.html", title="Contact")


@bp.get("/courses")
def courses() -> str:
    courses: List[Course] = Course.query.all()

    return render_template("main/pages/courses.html", title="Courses", courses=courses)


@bp.get("/search")
def search():
    return render_template("main/pages/result.html", title="Result")


@bp.post("/newsletter")
def newsletter():
    response: Response = Response(headers={"Content-Type": "application/json"})

    form = NewsletterForm()

    if form.validate_on_submit():
        print("sd")
    else:
        print(form.errors)

    return response
