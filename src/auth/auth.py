from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, get_raw_jwt
from redis import Redis
from database import UserDb

jwt = JWTManager()

@jwt.user_identity_loader
def user_identity_callback(user):
    return user.id  # 配置用户身份回调函数

@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return UserDb.getUserByID(identity)  # 配置用户加载回调函数

class Auth:
    def init_jwt(self, app: Flask, redis: Redis):
        app.config['JWT_SECRET_KEY'] = app.secret_key
        app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies']  # 指定Token的位置，例如在请求的Header和Cookie中
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600 * 24 * 3  # 设置Token的过期时间，单位为秒
        app.config['JWT_BLACKLIST_ENABLED'] = True  # 启用黑名单功能
        app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']  # 仅对访问令牌进行黑名单检查

        jwt.token_in_blacklist_loader(lambda decoded_token: decoded_token['jti'] in redis)  # 配置黑名单加载器
        jwt.init_app(app, redis_store=redis)

    # _md5Salt = "@^4_00wedv**pi)+(!w1rwi=d3q4l=ie=g-u$s8jevmj*zgg2h"
    # _salt = "@^4_00wedv**pi)+(!w1rwi=d3q4l=ie=g-u$s8jevmj*zgg2h"
    # _expire_message = dict(code=1200, msg="token过期")
    # _unknown_error_message = dict(code=9999, msg="token解析失败")

    def access_token(self, identify: int):
        return create_access_token(identity=identify)
    
    def user_identify(self) -> int:
        return int(get_jwt_identity())
    
    def logout():
        jti = get_raw_jwt()['jti']  # 获取当前Token的JTI（JWT ID）值
        blacklisted_tokens.add(jti)  # 将Token添加到黑名单中

    # @classmethod
    # def md5(cls, value: str) -> str:
    #     import hashlib
    #     return hashlib.md5(f"{value}-{cls._md5Salt}".encode("utf-8")).hexdigest()

    # @classmethod
    # def generate_token(cls, payload: dict) -> str:
    #     header = dict(type="JWT", alg="HS256")
    #     return jwt.encode(payload=payload, key=cls._salt, headers=header)
    
    # @classmethod
    # def parse_token(cls, token: str, issuer: str = None) -> tuple[dict, bool]:
    #     verify_status = False
    #     try:
    #         payload_data = jwt.decode(token, cls._salt, issuer=issuer, algorithms=["HS256"])
    #         verify_status = True
    #     except jwt.ExpiredSignatureError:
    #         payload_data = cls._expire_message
    #     except:
    #         payload_data = cls._unknown_error_message
    #     return payload_data, verify_status
    

    # @staticmethod
    # def auth_payload(data: dict, iss: str) -> dict:
    #     return  {
    #         "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7), #过期时间
    #         "iat": datetime.datetime.utcnow(),  #开始时间
    #         "iss": iss,
    #         "data": data,
    #     }



auth = Auth()