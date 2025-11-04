from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from rich.console import Console

# Instantiate extensions (no app yet)
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
console = Console()

login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"
