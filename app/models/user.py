import enum
from datetime import date
from typing import Dict

from flask import url_for
from flask_login import UserMixin

from app.constants import DEFAULT_AVATAR
from app.extensions import bcrypt, db, login_manager


@login_manager.user_loader
def load_user(user_id: str):
    return User.query.get(int(user_id))


class Role(enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    user_name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)

    password_hash = db.Column(db.String(128), nullable=False)

    birthday = db.Column(db.Date)
    role = db.Column(db.Enum(Role), default=Role.USER, nullable=False)

    # Files
    avatar_path = db.Column(
        db.String(255),
        nullable=True,
    )  # Path to avatar image

    def to_dict(self) -> Dict:
        dct = {
            "user_id": self.user_id,
            "first_name": self.first_name,
            "middle_name": self.middle_name,
            "last_name": self.last_name,
            "user_name": self.user_name,
            "email": self.email,
            "birthday": self.display_birthday,
            "age": self.age,
            "avatar": self.avatar_src,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

        return dct

    def get_id(self):
        return str(self.user_id)

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.generate_password_hash(password).decode()

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.user_name}>"

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
    def display_birthday(self):
        if self.birthday:
            return self.birthday.strftime("%Y-%m-%d")

        return "N/A"

    @property
    def avatar_src(self) -> str:
        if self.avatar_path:
            return self.avatar_path

        return url_for("static", filename=DEFAULT_AVATAR)
