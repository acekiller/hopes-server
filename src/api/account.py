from flask import Blueprint, request, make_response
from utils import ResponseData
from database.user_db import UserDb
from . import api
import app_tools

account_api = Blueprint("account_api", __name__, url_prefix='/v1/account')

@account_api.route("/login", methods=["POST"])
def login():
    '''
    用户登录接口
    '''
    phone = request.form.get("phone", type=str)
    if phone is None:
        return ResponseData.parameter_loss("phone")
    
    password = request.form.get("password", type=str)
    if password is None:
        return ResponseData.parameter_loss("password")
    
    user = UserDb.getUserByPhone(phone)
    if user is None:
        return ResponseData.dataNotExist(f"phone={phone}")
    
    if user.password != password:
        return ResponseData.custom_error(10001, "密码错误")

    (token, exp) = app_tools.generate_auth_token(user)
    formd = f"Bearer {token}"
    user_dict = ResponseData.model_to_dict(user, exclude_fields=["password", "phone"])
    resp = make_response(ResponseData.response_data(user_dict))
    resp.set_cookie("Authorization", formd, domain="127.0.0.1", expires=exp)
    return resp

@account_api.route("/register", methods=["POST"])
def register():
    '''
    用户注册接口
    '''
    if UserDb.userIsExists(request.json["phone"], request.json["username"]):
        return ResponseData.common_error("用户已存在")
    
    user = UserDb.addUser(request.json["phone"], request.json["username"], request.json["password"], request.json["nickname"])
    if user is None:
        return ResponseData.common_error("注册失败")
    
    token, exp = app_tools.generate_auth_token(user)
    formd = f"Bearer {token}"
    user_dict = ResponseData.model_to_dict(user, exclude_fields=["password", "phone"])
    resp = make_response(ResponseData.response_data(user_dict))
    resp.set_cookie("Authorization", formd, domain="127.0.0.1", expires=exp)
    return resp

@account_api.route("/logout", methods=["GET"])
def logout():
    '''
    用户退出登录接口
    '''
    app_tools.clear_auth_data()
    resp = make_response(ResponseData.response_data(None))
    resp.delete_cookie("Authorization")
    return resp

@account_api.route("/update", methods=["POST"])
def update():
    return "update"

@account_api.route("/modify", methods=["POST"])
def modify():
    return "modify"

@account_api.route("/updatePwd", methods=["GET"])
def updatePwd():
    return "updatePwd"

api.api_bp.register_blueprint(account_api)

__all__ = [
    "account_api",
]