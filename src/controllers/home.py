from .controllers import controller_bp
from flask import Blueprint, session, request
from flask import render_template
from app_tools import hopes_auth_check

home = Blueprint("home", __name__)

@home.route("/")
def index():
    return render_template("index.html")


controller_bp.register_blueprint(home)