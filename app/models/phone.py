from datetime import datetime, timezone

from app.extensions import db


class EmployeePhone(db.Model):
    __tablename__ = "employee_phones"

    phone_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(
        db.Integer, db.ForeignKey("employees.employee_id"), nullable=False
    )
    phone_number = db.Column(db.String(20), unique=True, nullable=False)

    employee = db.relationship("Employee", back_populates="phones")

    def to_dict(self) -> dict:
        return {
            "phone_id": self.phone_id,
            "employee_id": self.employee_id,
            "phone_number": self.phone_number,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<EmployeePhone {self.phone_number} Employee={self.employee_id}>"


class TeacherPhone(db.Model):
    __tablename__ = "teacher_phones"

    phone_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teacher_id = db.Column(
        db.Integer, db.ForeignKey("teachers.teacher_id"), nullable=False
    )
    phone_number = db.Column(db.String(20), unique=True, nullable=False)

    teacher = db.relationship("Teacher", back_populates="phones")

    def to_dict(self) -> dict:
        """Return a dictionary representation of the TeacherPhone."""
        return {
            "phone_id": self.phone_id,
            "teacher_id": self.teacher_id,
            "phone_number": self.phone_number,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<TeacherPhone {self.phone_number} Teacher={self.teacher_id}>"


class StudentPhone(db.Model):
    __tablename__ = "student_phones"

    phone_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(
        db.Integer, db.ForeignKey("students.student_id"), nullable=False
    )
    phone_number = db.Column(db.String(20), unique=True, nullable=False)

    student = db.relationship("Student", back_populates="phones")

    def to_dict(self) -> dict:
        """Return a dictionary representation of the StudentPhone."""
        return {
            "phone_id": self.phone_id,
            "student_id": self.student_id,
            "phone_number": self.phone_number,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f"<StudentPhone {self.phone_number} Student={self.student_id}>"
