from datetime import datetime, timezone

import humanize
from numerize.numerize import numerize

from app.constants import CURRENCY_SYMBOL
from app.extensions import db


class Payment(db.Model):
    __tablename__ = "payments"

    # Primary Key
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Foreign Key
    enrollment_id = db.Column(
        db.Integer, db.ForeignKey("enrollments.enrollment_id"), nullable=False
    )

    # Payment Info
    amount = db.Column(db.Numeric(12, 2), nullable=False)  # Payment amount
    payment_date = db.Column(
        db.Date, nullable=False, default=lambda: datetime.now(timezone.utc).date()
    )
    month_for = db.Column(
        db.String(20), nullable=True  # e.g., "2025-09" for the month being paid
    )

    # Relationship
    enrollment = db.relationship("Enrollment", back_populates="payments")

    @property
    def display_amount(self) -> str:
        return f"{CURRENCY_SYMBOL}{float(self.amount):,.2f}"

    @property
    def display_payment_date(self) -> str:
        return self.payment_date.strftime("%Y-%m-%d")

    @property
    def display_month_for(self) -> str:
        if not self.month_for:
            return "N/A"
        try:
            dt = datetime.strptime(self.month_for, "%Y-%m")
            return dt.strftime("%B %Y")
        except Exception:
            return self.month_for

    @property
    def relative_payment_time(self) -> str:
        try:
            dt = datetime.combine(self.payment_date, datetime.min.time())
            return humanize.naturaltime(datetime.now() - dt)
        except Exception:
            return "N/A"

    @classmethod
    def display_total(cls) -> str:
        amount: float = 0

        for p in cls.query.all():
            amount += p.amount

        return f"{CURRENCY_SYMBOL}{numerize(amount, 2)}"

    def to_dict(self) -> dict:
        return {
            "payment_id": self.payment_id,
            "enrollment_id": self.enrollment_id,
            "amount": float(self.amount),
            "payment_date": self.display_payment_date,
            "month_for": self.month_for,
        }

    def __repr__(self):
        return f"<Payment ID={self.payment_id} Enrollment={self.enrollment_id} Amount={self.amount}>"
