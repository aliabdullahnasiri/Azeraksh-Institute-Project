from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    PROJECT_TITLE: str = os.getenv("PROJECT_TITLE", "Azeraksh Institute")

    SECRET_KEY = os.getenv("SECRET_KEY", "12345678")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///dev.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"

    UPLOAD_FOLDER = os.path.join("app", "static", "uploads")

    CURRENCY_SYMBOL = chr(36)

    DEFAULT_AVATAR = "admin/assets/img/default-avatar.png"

    APP_DIR = "app"
