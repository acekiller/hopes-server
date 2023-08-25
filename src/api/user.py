from flask import Blueprint, request
from . import response_data as response_data
from database.user_db import UserDb
from . import api
from flask_jwt_extended import jwt_required
from auth import auth

user_api = Blueprint("user_api", __name__, url_prefix="/v1/user")

@user_api.route("follows", methods=["GET"])
@jwt_required
def follows():
    identify = auth.get_user_id()
    return response_data.response_data({"list": [], "count": None})

@user_api.route("/follows", methods=["POST"])
@jwt_required
def followsMe():
    identify = auth.get_user_id()
    return response_data.response_data({"list": [], "count": None})

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
    uid = int(argsId) if argsId is not None else int(auth.user_identify())
    if uid is None or uid <= 0:
        return response_data.notLogin()

    user = UserDb.getUserByID(uid)
    if user is None:
        return response_data.dataNotExist(f"id={uid}")
    
    return response_data.response_data(user)


api.api_bp.register_blueprint(user_api)