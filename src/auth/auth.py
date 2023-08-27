import datetime
from typing import Optional
from flask import Flask
from redis import Redis
import jwt

class Auth:
    def init_jwt(self, app: Flask, redis: Redis):
        app.config['JWT_SECRET_KEY'] = app.secret_key
        self._salt = app.secret_key
        self._md5Salt = app.secret_key

    _expire_message = dict(code=1200, msg="token过期")
    _unknown_error_message = dict(code=9999, msg="token解析失败")

    def md5(self, value: str) -> str:
        import hashlib
        return hashlib.md5(f"{value}-{self._md5Salt}".encode("utf-8")).hexdigest()

    # jwt数据编码
    def encode_payload(self, payload: dict, headers: dict = None) -> str:
        headers = {} if headers is None else headers
        headers["type"] = "JWT"
        return jwt.encode(payload=payload, key=self._salt, algorithm="HS256", headers=headers)
    
    # 对jwt编码的数据解码
    def parse_payload(self, token: str, issuer: str = None) -> tuple[dict, str, int, bool]:
        print(token, issuer)
        verify_status = False
        try:
            payload_data = jwt.decode(token, self._salt, issuer=issuer, algorithms=["HS256"], verify=False)
            verify_status = True
        except jwt.ExpiredSignatureError:
            payload_data = self._expire_message
        except Exception:
            payload_data = self._unknown_error_message
        
        print(payload_data, verify_status)
        return payload_data.get("data"), payload_data.get("iss"), payload_data.get("exp"), verify_status
    

    # jwt格式数据组装
    def generate_payload(self, data: dict, iss: str, maxAge: Optional[int] = None) -> dict:
        return {
            "exp": None if maxAge is None else datetime.datetime.utcnow() + datetime.timedelta(seconds=maxAge), #过期时间
            "iat": None if maxAge is None else datetime.datetime.utcnow(),  #开始时间
            "iss": iss,
            "data": data,
        }

auth = Auth()

__all__ = [
    "auth",
]