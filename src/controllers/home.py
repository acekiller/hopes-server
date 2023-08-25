from .controllers import controller_bp
from flask import Blueprint, session, request
from flask import render_template
from auth import Auth

home = Blueprint("home", __name__)

@home.route("/")
def index():
    token = session.get("token")
    if token is not None:
        payloadData = Auth.parse_token(token)
        print(payloadData)
    
    return render_template("index.html")


controller_bp.register_blueprint(home)