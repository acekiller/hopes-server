from models.user import User
from auth import Auth
from database.user_db import UserDb

def user_auth_payload(user: User, iss: str, client: str = None) -> dict:
    return Auth.auth_payload(data={
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "client": client,
        }, iss=iss)
    

def generate_user_token(user: User) -> str:
    payload = user_auth_payload(user, iss=Auth.md5(f"{user.id}{user.password}"))
    return Auth.generate_token(payload)


def parse_user_token(token: str, user: User) -> tuple[dict, bool]:
    return Auth.parse_token(token, issuer=Auth.md5(f"{user.id}{user.password}"))

def isLoggedIn(session) -> bool:
    token = session.get("token")
    uid = session.get("identifier")
    if uid is None:
        return False

    if token is None:    
        return False

    user = UserDb.getUserByID(int(uid))
    if user is None:
        return False

    result = parse_user_token(token, user)
    return result[1]

def getUserID(session) -> int:
    return int(session.get("identifier"))