import pathlib
from datetime import datetime, timezone
from typing import Optional, Self

import humanize

from app.constants import APP_DIR
from app.extensions import db


class FileMixin(object):
    pass


class File(db.Model):
    __tablename__ = "files"

    # Primary Key
    file_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # File Info
    file_name = db.Column(
        db.String(255),
        nullable=False,
        default=lambda: datetime.now(timezone.utc).date(),
    )
    file_description = db.Column(db.String(255))
    file_for = db.Column(db.String(25))
    file_url = db.Column(db.String(255), nullable=False)

    @property
    def path(self: Self) -> pathlib.Path:
        return pathlib.Path(f"{APP_DIR}/{self.file_url}")

    @property
    def exists(self: Self) -> bool:
        return self.path.exists()

    @property
    def size(self: Self) -> int:
        try:
            return self.path.stat().st_size if self.exists else 0
        except OSError:
            return 0

    @property
    def human_size(self: Self) -> str:
        return humanize.naturalsize(self.size) if self.size else "0 B"

    @property
    def extension(self: Self) -> Optional[str]:
        return self.path.suffix.lstrip(".").upper() if self.path.suffix else None

    @property
    def display_name(self: Self) -> str:
        return (
            f"{self.file_name}.{self.extension.lower()}"
            if self.extension
            else self.file_name
        )

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

    def to_dict(self) -> dict:
        return {
            "file_id": self.file_id,
            "file_name": self.file_name,
            "file_description": self.file_description,
            "file_for": self.file_for,
            "file_url": self.file_url,
            "extension": self.extension,
            "size": self.size,
            "human_size": self.human_size,
            "exists": self.exists,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<File {self.file_name} ({self.human_size}) ID={self.file_id}>"


class TeacherFile(db.Model):
    __tablename__ = "teacher_files"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher_id = db.Column(
        db.Integer, db.ForeignKey("teachers.teacher_id"), nullable=False
    )
    file_id = db.Column(
        db.Integer, db.ForeignKey("files.file_id"), nullable=False, unique=True
    )

    file = db.relationship("File")
    teacher = db.relationship("Teacher", back_populates="files")

    def __repr__(self):
        return f"<TeachertFile ID={self.id} TeacherID={self.teacher_id} FileID={self.file_id}>"


class CourseFile(db.Model):
    __tablename__ = "course_files"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(
        db.Integer, db.ForeignKey("courses.course_id"), nullable=False
    )
    file_id = db.Column(
        db.Integer, db.ForeignKey("files.file_id"), nullable=False, unique=True
    )

    file = db.relationship("File")
    course = db.relationship("Course", back_populates="files")

    def __repr__(self):
        return (
            f"<CourseFile ID={self.id} CourseID={self.course_id} FileID={self.file_id}>"
        )


class StudentFile(db.Model):
    __tablename__ = "student_files"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(
        db.Integer, db.ForeignKey("students.student_id"), nullable=False
    )
    file_id = db.Column(
        db.Integer, db.ForeignKey("files.file_id"), nullable=False, unique=True
    )

    file = db.relationship("File")
    student = db.relationship("Student", back_populates="files")

    def __repr__(self):
        return f"<StudentFile ID={self.id} StudentID={self.student_id} FileID={self.file_id}>"
