from flask import Blueprint
from .controllers import controller_bp

abouts = Blueprint("abouts", __name__, url_prefix="/abouts")

@abouts.route("/")
def index():
    return "关于我们"

controller_bp.register_blueprint(abouts)