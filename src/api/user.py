from flask import Blueprint, request
from utils import ResponseData
from database.user_db import UserDb
from . import api
import app_tools

user_api = Blueprint("user_api", __name__, url_prefix="/v1/user")

@user_api.route("follows", methods=["GET"])
@app_tools.hopes_auth_check()
def follows():
    # identify = utils.current_user_id()
    return ResponseData.response_data({"list": [], "count": None})

@user_api.route("/follow", methods=["POST"])
@app_tools.hopes_auth_check()
def follow_me():
    # identify = utils.current_user_id()
    return ResponseData.response_data({"list": [], "count": None})

@user_api.route("/info", methods=["GET"])
def detail():
    '''
    用户信息详情接口
    parameters:
    - user_id: 用户id
      in: query
      required: true
      type: integer
    responses:
    - 200:
      description: success
      schema:
        code: 0
        data:
            id: integer
            username: string
            nickname: string
    '''
    argsId = request.args.get("id", type=int)
    uid = int(argsId) if argsId is not None else utils.current_user_id()
    if uid is None or uid <= 0:
        return ResponseData.notLogin()

    user = UserDb.getUserByID(uid)
    if user is None:
        return ResponseData.dataNotExist(f"id={uid}")
    
    return ResponseData.response_data(user)


api.api_bp.register_blueprint(user_api)

__all__ = [
    "user_api",
]