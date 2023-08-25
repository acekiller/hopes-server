from flask import Flask
from database import mdb
from auth import auth
from redis import Redis

app = Flask(__name__)
redis_store = Redis(host='localhost', port=6379, db=0)

class App():
    @classmethod
    def create_app(cls):
        app.secret_key = 'cgadafe0129018'
        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{mdb.user}:{mdb.password}@{mdb.host}:{mdb.port}/{mdb.database}?charset=utf8mb4"
        app.config['SQLALCHEMY_ECHO'] = True
        app.config['JSON_AS_ASCII'] = False
        app.config['JWT_SECRET_KEY'] = app.secret_key
        mdb.db.init_app(app)
        auth.init_jwt(app=app, redis=redis_store)
        return app
    
    @classmethod
    def create_app_db(cls):
        mdb.db.create_all(app=cls.create_app())