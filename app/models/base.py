import random
from datetime import datetime, timedelta, timezone

from numerize import numerize
from sqlalchemy import Column, Integer, String, event, extract, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from app.extensions import db


class Base(db.Model):
    __abstract__ = True

    @declared_attr
    def uid(cls):
        return Column(String(8), unique=True, nullable=False)

    # Timestamps
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def get_display_value(self, attr):
        value = getattr(self, attr, None)
        return "N/A" if value is None else value

    @classmethod
    def weekly_growth_clr(cls):
        if cls.weekly_growth() > 0:
            return "success"

        return "danger"

    @classmethod
    def weekly_growth(cls):
        now = datetime.now(timezone.utc)

        start_of_week = datetime.combine(
            (now - timedelta(days=now.weekday())).date(),
            datetime.min.time(),
            tzinfo=timezone.utc,
        )
        start_of_last_week = start_of_week - timedelta(weeks=1)
        end_of_last_week = start_of_week

        current_week = (
            db.session.query(cls).filter(cls.created_at >= start_of_week).count()
        )

        previous_week = (
            db.session.query(cls)
            .filter(
                cls.created_at >= start_of_last_week, cls.created_at < end_of_last_week
            )
            .count()
        )

        return cls._percent_change(current_week, previous_week)

    @classmethod
    def display_weekly_growth(cls):
        sign = chr(43) if cls.weekly_growth() > 0 else chr(45)
        growth = f"{sign}{abs(cls.weekly_growth())}{chr(37)}"

        return growth

    @classmethod
    def monthly_growth(cls):
        current_month = datetime.now().month
        last_month = current_month - 1 if current_month > 1 else 12

        current_count = (
            db.session.query(func.count(cls.created_at))
            .filter(extract("month", cls.created_at) == current_month)
            .scalar()
        )

        previous_count = (
            db.session.query(func.count(cls.created_at))
            .filter(extract("month", cls.created_at) == last_month)
            .scalar()
        )

        return cls._percent_change(current_count, previous_count)

    @classmethod
    def monthly_growth_clr(cls):
        if cls.monthly_growth() > 0:
            return "success"

        return "danger"

    @classmethod
    def display_monthly_growth(cls):
        sign = chr(43) if cls.monthly_growth() > 0 else chr(45)
        growth = f"{sign}{abs(cls.monthly_growth())}{chr(37)}"

        return growth

    @staticmethod
    def _percent_change(current, previous):
        if previous == 0:
            return 100 if current > 0 else 0
        return round(((current - previous) / previous) * 100, 2)

    @classmethod
    def count(cls):
        return numerize.numerize(cls.query.count(), 2)


@event.listens_for(Base, "before_insert", propagate=True)
def generate_uid(mapper, connection, target):
    prefix = target.__class__.__name__[0].upper()  # First letter of class name
    random_number = random.randint(100000, 999999)
    target.uid = f"{prefix}-{random_number}"


db.Model = Base
