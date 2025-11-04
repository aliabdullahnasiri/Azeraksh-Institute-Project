import os
import tempfile

import pytest

from app import create_app
from app.extensions import db


@pytest.fixture()
def app():
    # use a temp SQLite DB for testing
    db_fd, db_path = tempfile.mkstemp()
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

    app = create_app()
    with app.app_context():
        db.create_all()
    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture()
def client(app):
    return app.test_client()
