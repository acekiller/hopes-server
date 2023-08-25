from api import api_bp
from flask import Blueprint

forum_bp = Blueprint("forum_bp", __name__, url_prefix="/v1/forum")

@forum_bp.before_request
def before_request():
    pass

@forum_bp.route("publish", methods=["POST"])
def publish():
    pass

@forum_bp.route("commment", methods=["POST"])
def commment():
    pass

@forum_bp.route("list", methods=["GET"])
def list():
    pass

@forum_bp.route("commmentList", methods=["POST"])
def commmentList():
    pass

@forum_bp.route("detail", methods=["GET"])
def detail():
    pass

@forum_bp.route("likes", methods=["POST", "GET"])
def like():
    pass

api_bp.register_blueprint(api_bp)