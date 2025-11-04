from datetime import date, datetime, timezone

import humanize
from flask import url_for

from app.constants import CURRENCY_SYMBOL, DEFAULT_AVATAR
from app.extensions import db


class Teacher(db.Model):
    __tablename__ = "teachers"

    # Primary Key
    teacher_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Personal Info
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    birthday = db.Column(db.Date, nullable=True)

    avatar_path = db.Column(db.String(255), nullable=True)  # Path to avatar image
    salary = db.Column(db.Numeric(12, 2), nullable=True)

    # Relationship
    courses = db.relationship(
        "Course", back_populates="teacher", cascade="all, delete, delete-orphan"
    )
    phones = db.relationship(
        "TeacherPhone", back_populates="teacher", cascade="all, delete, delete-orphan"
    )
    files = db.relationship(
        "TeacherFile", back_populates="teacher", cascade="all, delete, delete-orphan"
    )

    @property
    def full_name(self) -> str:
        parts = [self.first_name]
        if self.middle_name:
            parts.append(self.middle_name)
        parts.append(self.last_name)
        return " ".join(parts)

    @property
    def age(self) -> int | None:
        if self.birthday is None:
            return None
        today = date.today()
        return (
            today.year
            - self.birthday.year
            - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
        )

    @property
    def display_birthday(self) -> str:
        return self.birthday.strftime("%Y-%m-%d") if self.birthday else "N/A"

    @property
    def display_salary(self) -> str:
        return (
            f"{CURRENCY_SYMBOL}{float(self.salary):,.2f}"
            if self.salary is not None
            else "N/A"
        )

    @property
    def total_file_size(self) -> str:
        total: int = 0
        for f in self.files:
            total += f.file.size
        return humanize.naturalsize(total)

    @property
    def total_students_count(self) -> int:
        total: int = 0

        for course in self.courses:
            total = total + len(course.enrollments)

        return total

    @property
    def is_salary_gt_avg(self) -> bool:
        teachers = self.query.all()
        salaries = [float(t.salary) for t in teachers if t.salary is not None]
        if not salaries or self.salary is None:
            return False
        avg_salary = sum(salaries) / len(salaries)
        return float(self.salary) > avg_salary

    @property
    def display_created_at(self) -> str:
        return (
            self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else "N/A"
        )

    @property
    def display_updated_at(self) -> str:
        return (
            self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at else "N/A"
        )

    @property
    def avatar_src(self) -> str:
        if self.avatar_path:
            return self.avatar_path

        return url_for("static", filename=DEFAULT_AVATAR)

    def to_dict(self):
        dct = {
            "teacher_id": self.teacher_id,
            "full_name": self.full_name,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "email": self.email,
            "birthday": self.display_birthday,
            "age": self.age,
            "salary": f"{self.salary:.2f}" if self.salary is not None else None,
            "avatar": self.avatar_path,
            "phones": [p.phone_number for p in self.phones],
            "files": [f.file.to_dict() for f in self.files],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

        return dct

    def __repr__(self):
        return f"<Teacher {self.full_name} ID={self.teacher_id}>"
