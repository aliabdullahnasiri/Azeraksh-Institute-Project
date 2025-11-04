from flask import Blueprint

bp: Blueprint = Blueprint("init", __name__)

from app.blueprints.init import main
