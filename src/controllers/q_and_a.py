from flask import Blueprint
from .controllers import controller_bp

qa = Blueprint("qa", __name__, url_prefix="/qa")

@qa.route("/")
def index():
    return "QA"

controller_bp.register_blueprint(qa)