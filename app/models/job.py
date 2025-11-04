from datetime import datetime, timezone
from decimal import Decimal
from typing import Dict

from app.constants import CURRENCY_SYMBOL
from app.extensions import db


class Job(db.Model):
    __tablename__ = "jobs"

    job_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text, nullable=True)
    min_salary = db.Column(db.Numeric(12, 2), nullable=False)
    max_salary = db.Column(db.Numeric(12, 2), nullable=False)

    employees = db.relationship(
        "Employee", back_populates="job", cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return f"<Job {self.job_title} ID={self.job_id}>"

    def to_dict(self) -> Dict:
        dct = {
            "job_id": self.job_id,
            "job_title": self.job_title,
            "job_description": self.job_description,
            "min_salary": f"{self.min_salary:.2f}",
            "max_salary": f"{self.min_salary:.2f}",
            "created_at": self.display_created_at,
            "updated_at": self.display_updated_at,
        }

        return dct

    @property
    def employee_count(self) -> int:
        return len(self.employees)

    @property
    def average_salary(self) -> float | None:
        if not self.employees:
            return None
        total_salary = sum([float(emp.salary or 0) for emp in self.employees])
        return total_salary / len(self.employees)

    @property
    def highest_salary(self) -> float | None:
        if not self.employees:
            return None
        return max([float(emp.salary or 0) for emp in self.employees])

    @property
    def lowest_salary(self) -> float | None:
        if not self.employees:
            return None
        return min([float(emp.salary or 0) for emp in self.employees])

    @property
    def display_min_salary(self) -> str:
        if type(self.min_salary) is Decimal:
            return f"{CURRENCY_SYMBOL}{self.min_salary:.2f}"

        return "N/A"

    @property
    def display_max_salary(self) -> str:
        if type(self.max_salary) is Decimal:
            return f"{CURRENCY_SYMBOL}{self.max_salary:.2f}"

        return "N/A"

    @property
    def display_salary_range(self) -> str:
        if self.min_salary and self.max_salary:
            return f"{CURRENCY_SYMBOL}{self.min_salary:,.2f} - {CURRENCY_SYMBOL}{self.max_salary:,.2f}"
        elif self.min_salary:
            return f"{CURRENCY_SYMBOL}{self.min_salary:,.2f} and up"
        elif self.max_salary:
            return f"Up to {CURRENCY_SYMBOL}{self.max_salary:,.2f}"
        return "N/A"

    @property
    def display_average_salary(self) -> str:
        if self.average_salary is None:
            return "N/A"
        return f"{CURRENCY_SYMBOL}{self.average_salary:,.2f}"

    @property
    def display_highest_salary(self) -> str:
        if self.highest_salary is None:
            return "N/A"
        return f"{CURRENCY_SYMBOL}{self.highest_salary:,.2f}"

    @property
    def display_lowest_salary(self) -> str:
        if self.lowest_salary is None:
            return "N/A"
        return f"{CURRENCY_SYMBOL}{self.lowest_salary:,.2f}"

    @property
    def display_job_id(self) -> str:
        return str(self.job_id)

    @property
    def display_title(self) -> str:
        return self.job_title or "N/A"

    @property
    def display_description(self) -> str:
        return self.job_description or "No description"

    @property
    def display_employee_count(self) -> str:
        return str(self.employee_count)

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
