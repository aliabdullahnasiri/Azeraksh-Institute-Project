from typing import Any, Dict

from sqlalchemy import and_

from app.constants import CURRENCY_SYMBOL
from app.extensions import db
from app.models.enrollment import EnrollmentStatus
from app.models.file import CourseFile, File


class Course(db.Model):
    __tablename__ = "courses"

    # Primary Key
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign Key
    teacher_id = db.Column(
        db.Integer, db.ForeignKey("teachers.teacher_id"), nullable=False
    )

    # Course Info
    course_title = db.Column(db.String(100), nullable=False)
    course_description = db.Column(db.Text, nullable=True)

    # Schedule
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)

    # Financials
    monthly_fee = db.Column(db.Numeric(12, 2), nullable=True)

    # Relationships
    teacher = db.relationship("Teacher", back_populates="courses")
    enrollments = db.relationship(
        "Enrollment", back_populates="course", cascade="all, delete, delete-orphan"
    )
    files = db.relationship(
        "CourseFile", back_populates="course", cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return f"<Course {self.course_title} ID={self.course_id}>"

    @property
    def display_start_date(self) -> str:
        """Formatted start date (YYYY-MM-DD)."""
        return self.start_date.strftime("%Y-%m-%d") if self.start_date else "N/A"

    @property
    def display_end_date(self) -> str:
        return self.end_date.strftime("%Y-%m-%d") if self.end_date else "N/A"

    @property
    def display_start_time(self) -> str:
        return self.start_time.strftime("%H:%M") if self.start_time else "N/A"

    @property
    def display_end_time(self) -> str:
        return self.end_time.strftime("%H:%M") if self.end_time else "N/A"

    @property
    def display_monthly_fee(self) -> str:
        if self.monthly_fee is None:
            return "N/A"

        return f"{CURRENCY_SYMBOL}{self.monthly_fee:,.2f}"

    @property
    def display_teacher_name(self) -> str:
        if self.teacher:
            return self.teacher.full_name

        return "N/A"

    @property
    def active_enrollments_count(self) -> int:
        """Count of active enrollments."""
        return len(
            [
                e
                for e in self.enrollments
                if e.status.value == EnrollmentStatus.ACTIVE.value
            ]
        )

    @property
    def closed_enrollments_count(self) -> int:
        """Count of closed enrollments."""
        return len(
            [
                e
                for e in self.enrollments
                if e.status.value == EnrollmentStatus.CLOSED.value
            ]
        )

    @property
    def monthly_earnings(self) -> float:
        total = sum(
            [
                float(e.monthly_fee or 0)
                for e in self.enrollments
                if e.status == EnrollmentStatus.ACTIVE
            ]
        )
        return round(total, 2)

    @property
    def display_monthly_earnings(self) -> str:
        return f"{CURRENCY_SYMBOL}{self.monthly_earnings}"

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

    def to_dict(self) -> Dict[str, Any]:
        return {
            "course_id": self.course_id,
            "teacher_id": self.teacher_id,
            "course_title": self.course_title,
            "course_description": self.course_description,
            "monthly_fee": f"{self.monthly_fee:.2f}" if self.monthly_fee else None,
            "start_date": self.display_start_date,
            "end_date": self.display_end_date,
            "start_time": self.display_start_time,
            "end_time": self.display_end_time,
            "files": [f.file.to_dict() for f in self.files],
            "created_at": self.display_created_at,
            "updated_at": self.display_updated_at,
        }

    @property
    def banner(self):
        if files := [f for f in self.files if f.file.file_for == "banner"]:
            return files.pop().file
