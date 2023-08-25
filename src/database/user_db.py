from database.mdb import db
from models.user import User

class UserDb():
    @classmethod
    def addUser(cls, phone: str, username: str, password: str, nickname: str):
        if cls.userIsExists(phone, username):
            return None
        user = User(phone=phone, username=username, password=password, nickname=nickname)
        db.session.add(user)
        db.session.commit()
        return user.id

    @classmethod
    def userIsExists(cls, phone: str, username: str):
        return True if db.session.query(User.phone).filter_by(phone=phone).count() > 0 else db.session.query(User.username).filter_by(username=username).count() > 0
    
    @classmethod
    def getUserByID(cls, id: int):
        return db.session.query(User).filter_by(id=id).first()

    @classmethod
    def getUserByPhone(cls, phone: str):
        return db.session.query(User).filter_by(phone=phone).first()