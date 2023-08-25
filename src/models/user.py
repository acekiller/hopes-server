from database.mdb import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(32))
    username = db.Column(db.String(20), unique=True)
    nickname = db.Column(db.String(20))

    def __repr__(self):
        return '<User %r>' % self.username
    