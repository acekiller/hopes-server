import time
from typing import Optional
from models.user import User
from auth import auth
from flask import current_app, request
from functools import wraps
from auth_storage import UserAuthStorage
import datetime
from utils import clear_none_data

defaultMaxAge = 7 * 24 * 60 * 60
refreshDelta = 60 * 3


class AuthException(Exception):
    def __init__(self, code: int, msg: str, *args: object) -> None:
        self.code = code
        self.msg = msg
        super().__init__(*args)

def verify(refresh: bool):
    token = request.cookies.get("Authorization").split(" ")[1]
    (data, _, _, isAuth) = auth.parse_payload(token=token)
    if isAuth == False:
        raise AuthException(401, "token验证失败")

    user = UserAuthStorage.get_auth_info(id=data.get("id"))
    last_expires = int(user.get("exp", 0))
    if user is None:
        raise AuthException(401, "用户信息有误")

    un_time = timestamp(datetime.datetime.now())
    if last_expires <= un_time:
        raise AuthException(401, "token过期")


def generate_auth_token(user: User, maxAge: int = None) -> tuple[str, datetime.datetime]:
    payload = auth.generate_payload(data={
        "id": user.id,
        }, iss=f"{user.id}{user.username}", maxAge=None)
    
    token = auth.encode_payload(clear_none_data(payload))
    maxAge = maxAge if maxAge is not None else defaultMaxAge
    exipres = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=maxAge)
    exipresTimestamp = timestamp(exipres)
    user_info = {"id": user.id, "token": token, "exp": exipresTimestamp}
    UserAuthStorage.save_auth_info(value=user_info, id=user.id, expires=maxAge)
    return (token, exipres)


def current_user_id() -> int:
    token = request.headers.get("Authorization")
    (data, _, _, isAuth) = auth.parse_payload(token=token)
    return data.get("id") if isAuth else 0


def clear_auth_data():
    authorization = request.cookies.get("Authorization")
    if authorization is None:
        return
    
    token = authorization.split(" ")[1]
    if token is None:
        return
    
    (data, iss, _, isAuth) = auth.parse_payload(token=token)
    if isAuth == False:
        return
    UserAuthStorage.delete_auth_info(data.get("id"))


def hopes_auth_check(refresh: bool = False):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify(refresh=refresh)
            return current_app.ensure_sync(fn)(*args, **kwargs)
        return decorator
    return wrapper

def refresh_or_generate_Token(id: int, token: Optional[str], iss: str = None, maxAge: Optional[int] = None, isCreate: bool = False) -> Optional[tuple[str, datetime.datetime]]:
    user = UserAuthStorage.get_auth_info(id=id)

    if not bool(user) or not bool(token):
        return None
    
    lastExpires = int(user.get("exp", 0))
    nowTimestamp = timestamp(datetime.datetime.now(datetime.timezone.utc))
    if lastExpires <= nowTimestamp:
        return None
    
    if lastExpires - nowTimestamp > refreshDelta:
        return None

    maxAge = maxAge if maxAge is not None else defaultMaxAge
    exipres = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=maxAge)
    exiprestimestamp = timestamp(exipres)

    user_info = {"id": id, "token": token, "exp": exiprestimestamp}
    UserAuthStorage.save_auth_info(value=user_info, id=id, expires=maxAge)
    return (token, exipres)


def refreshToken(token: str) -> Optional[tuple[str, datetime.datetime]]:
    if token is None:
        return None
    (data, iss, _, isAuth) = auth.parse_payload(token=token)
    if isAuth == False:
        return None
    return refresh_or_generate_Token(id=data.get("id"), token=token, iss=iss)


def timestamp(dtime: datetime.datetime) -> int:
    return int(time.mktime(dtime.timetuple()))


def refreshTokenIfNeed(response):
    authorization = request.cookies.get("Authorization")
    if authorization is None:
        return response
    
    token = authorization.split(" ")[1]
    result = refreshToken(token)
    if result is not None:
        response.set_cookie("Authorization", result[0], domain="127.0.0.1", expires=result[1])
    


__all__ = [
    "generate_auth_token",
    "clear_auth_data",
    "hopes_auth_check",
    "current_user_id",
    "refreshTokenIfNeed",
    "AuthException",
]
