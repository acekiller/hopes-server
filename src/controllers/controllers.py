from create_app import app
from flask import Blueprint

controller_bp = Blueprint("controller", __name__, url_prefix="/")
