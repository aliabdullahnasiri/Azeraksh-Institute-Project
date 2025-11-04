from datetime import date, datetime, timezone

import humanize
from flask import url_for

from app.constants import DEFAULT_AVATAR
from app.extensions import db
from app.models.enrollment import EnrollmentStatus


class Student(db.Model):
    __tablename__ = "students"

    # Primary Key
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Personal Info
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    birthday = db.Column(db.Date, nullable=True)

    # Files
    avatar_path = db.Column(db.String(255), nullable=True)  # Path to avatar image

    # Relationship
    enrollments = db.relationship(
        "Enrollment", back_populates="student", cascade="all, delete, delete-orphan"
    )
    phones = db.relationship(
        "StudentPhone", back_populates="student", cascade="all, delete, delete-orphan"
    )
    files = db.relationship(
        "StudentFile", back_populates="student", cascade="all, delete, delete-orphan"
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
    def total_files_size(self) -> str:
        total = sum((f.file.size for f in self.files), start=0)
        return humanize.naturalsize(total)

    @property
    def active_enrollments_count(self) -> int:
        return len([e for e in self.enrollments if e.status == EnrollmentStatus.ACTIVE])

    @property
    def closed_enrollments_count(self) -> int:
        return len([e for e in self.enrollments if e.status == EnrollmentStatus.CLOSED])

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

    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "email": self.email,
            "birthday": self.display_birthday,
            "age": self.age,
            "avatar": self.avatar_path,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "phones": [phone.phone_number for phone in self.phones],
            "files": [f.file.to_dict() for f in self.files],
            "enrollments": [enrollment.to_dict() for enrollment in self.enrollments],
        }

    def __repr__(self):
        return f"<Student {self.full_name} ID={self.student_id}>"
