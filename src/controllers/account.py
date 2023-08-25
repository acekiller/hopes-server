from flask import Blueprint, request, render_template
from .controllers import controller_bp

c_account_api = Blueprint("account_api", __name__, url_prefix="/user", template_folder="templates")

@c_account_api.route("login", methods=["GET"])
def login():
    return render_template("login.html")
        


controller_bp.register_blueprint(c_account_api)