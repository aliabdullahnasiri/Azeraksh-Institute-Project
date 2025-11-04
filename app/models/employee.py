from datetime import date, datetime, timezone

from flask import url_for

from app.constants import CURRENCY_SYMBOL, DEFAULT_AVATAR
from app.extensions import db


class Employee(db.Model):
    __tablename__ = "employees"

    # Primary Key
    employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign Keys
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.job_id"), nullable=True)

    # Personal Info
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True, index=True)
    birthday = db.Column(db.Date, nullable=True)

    # Files
    avatar_path = db.Column(
        db.String(255),
        nullable=True,
    )  # Path to avatar image

    # Employment Info
    address = db.Column(db.String(255), nullable=True)
    salary = db.Column(db.Numeric(12, 2), nullable=True)
    hire_date = db.Column(
        db.Date, nullable=False, default=datetime.now(timezone.utc).date
    )

    # Relationships
    job = db.relationship("Job", back_populates="employees")
    phones = db.relationship(
        "EmployeePhone", back_populates="employee", cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return f"<Employee {self.first_name} {self.last_name} ID={self.employee_id}>"

    def to_dict(self):
        dct = {
            "employee_id": self.employee_id,
            "job_id": self.job_id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "email": self.email,
            "birthday": self.display_birthday,
            "age": self.age,
            "avatar": self.avatar_path,
            "address": self.address,
            "salary": f"{self.salary:.2f}",
            "hire_date": self.display_hire_date,
            "created_at": self.display_created_at,
            "updated_at": self.display_updated_at,
            "phones": [phone.phone_number for phone in self.phones],
        }

        return dct

    # Derived attribute (not stored in DB)
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
    def is_salary_gt_avg(self) -> bool:
        employees = self.query.all()
        lst = [employee.salary.__int__() for employee in employees]
        average_salary = sum(lst) / len(lst)

        return self.salary > average_salary

    # --- Display properties for templates ---
    @property
    def full_name(self) -> str:
        """Return full name with middle name if exists."""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"

    @property
    def display_salary(self) -> str:
        """Display salary with currency symbol."""
        if self.salary is None:
            return "N/A"
        return f"{CURRENCY_SYMBOL}{float(self.salary):,.2f}"

    @property
    def display_hire_date(self) -> str:
        return self.hire_date.strftime("%Y-%m-%d") if self.hire_date else "N/A"

    @property
    def display_birthday(self) -> str:
        return self.birthday.strftime("%Y-%m-%d") if self.birthday else "N/A"

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
    def display_address(self) -> str:
        return self.address or "N/A"

    @property
    def display_email(self) -> str:
        return self.email or "N/A"

    @property
    def avatar_src(self) -> str:
        if self.avatar_path:
            return self.avatar_path

        return url_for("static", filename=DEFAULT_AVATAR)
