from create_app import app
from flask import Blueprint

api_bp = Blueprint("api_bp", __name__, url_prefix="/api")

__all__ = [
    "api_bp",
]