from flask import Blueprint, request
from api import response_data
from auth import auth
from database.user_db import UserDb
from . import api

account_api = Blueprint("account_api", __name__, url_prefix='/v1/account')

@account_api.route("/login", methods=["POST"])
def login():
    '''
    用户登录接口
    '''
    phone = request.form.get("phone", type=str)
    if phone is None:
        return response_data.parameter_loss("phone")
    
    password = request.form.get("password", type=str)
    if password is None:
        return response_data.parameter_loss("password")
    
    user = UserDb.getUserByPhone(phone)
    if user is None:
        return response_data.dataNotExist(f"phone={phone}")
    
    if user.password != password:
        return response_data.custom_error(10001, "密码错误")
    
    token = auth.access_token(user.id)
    user_dict = response_data.model_to_dict(user, exclude_fields=["password", "phone"])
    result = {"token": token, "user": user_dict}
    print(result)
    return response_data.response_data(result)


@account_api.route("/register", methods=["POST"])
def register():
    '''
    用户注册接口
    '''
    if UserDb.userIsExists(request.json["phone"], request.json["username"]):
        return response_data.common_error("用户已存在")
    
    user = UserDb.addUser(request.json["phone"], request.json["username"], request.json["password"], request.json["nickname"])
    if user is None:
        return response_data.common_error("注册失败")
    
    token = auth.access_token(user.id)
    user_dict = response_data.model_to_dict(user, exclude_fields=["password", "phone"])
    result = {"token": token, "user": user_dict}
    print(result)
    return response_data.response_data(result)

@account_api.route("/logout", methods=["POST"])
def logout():
    '''
    用户退出登录接口
    '''
    auth.logout()
    return response_data(None)

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