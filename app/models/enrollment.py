import enum
from datetime import datetime, timezone

from sqlalchemy import UniqueConstraint

from app.constants import CURRENCY_SYMBOL
from app.extensions import db


class EnrollmentStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"


class Enrollment(db.Model):

    __tablename__ = "enrollments"

    # Primary Key
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign Keys
    student_id = db.Column(
        db.Integer, db.ForeignKey("students.student_id"), nullable=False
    )
    course_id = db.Column(
        db.Integer, db.ForeignKey("courses.course_id"), nullable=False
    )

    # Enrollment Info
    enrollment_date = db.Column(
        db.Date, nullable=False, default=lambda: datetime.now(timezone.utc).date()
    )
    discount_rate = db.Column(db.Numeric(5, 2), nullable=True)  # e.g., 10.00 for 10%
    status = db.Column(
        db.Enum(EnrollmentStatus), nullable=False, default=EnrollmentStatus.ACTIVE
    )

    # Relationships
    student = db.relationship("Student", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")
    payments = db.relationship(
        "Payment", back_populates="enrollment", cascade="all, delete, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("student_id", "course_id", name="uix_student_course"),
    )

    @property
    def monthly_fee(self):
        m = self.course.monthly_fee
        return round(m - (m / 100 * self.discount_rate), 2)

    @property
    def monthly_discount(self):
        m = self.course.monthly_fee
        return m - self.monthly_fee

    @property
    def is_paid_this_month(self) -> bool:
        """Check if this student has paid for the current month."""
        current_month = datetime.now().strftime("%Y-%m")
        return any(payment.month_for == current_month for payment in self.payments)

    @property
    def total_payments(self):
        total = 0

        for payment in self.payments:
            total += payment.amount

        return total

    @property
    def display_discount_rate(self) -> str:
        if self.discount_rate:
            return f"{self.discount_rate:.2f}%"

        return f"N/A"

    @property
    def display_monthly_discount(self) -> str:
        return f"{CURRENCY_SYMBOL}{self.monthly_discount}"

    @property
    def display_monthly_fee(self):
        return f"{CURRENCY_SYMBOL}{self.monthly_fee}"

    @property
    def display_total_payments(self):
        return f"{CURRENCY_SYMBOL}{self.total_payments}"

    @property
    def display_status(self) -> str:
        return self.status.value

    @property
    def display_enrollment_date(self) -> str:
        return self.enrollment_date.strftime("%Y-%m-%d")

    def to_dict(self) -> dict:
        return {
            "enrollment_id": self.enrollment_id,
            "student_id": self.student_id,
            "course_id": self.course_id,
            "enrollment_date": self.enrollment_date.isoformat(),
            "discount_rate": f"{self.discount_rate:.2f}" if self.discount_rate else 0.0,
            "status": self.status.value,
        }

    def __repr__(self):
        return f"<Enrollment ID={self.enrollment_id} Student={self.student_id} Course={self.course_id}>"
