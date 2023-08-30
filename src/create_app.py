from flask import Flask
from flask_cors import CORS
from database import mdb
from auth import auth
from auth_storage import redis_store
import config as config

app = Flask(__name__)

class App():
    @classmethod
    def create_app(cls):
        CORS(app=app, supports_credentials=True)
        app.secret_key = config.app_key
        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{config.mysql_user}:{config.mysql_password}@{config.mysql_host}:{config.mysql_port}/{config.mysql_database}?charset=utf8mb4"
        app.config['SQLALCHEMY_ECHO'] = True
        app.config['JSON_AS_ASCII'] = False
        app.config['JWT_SECRET_KEY'] = app.secret_key
        mdb.db.init_app(app)
        auth.init_jwt(app=app, redis=redis_store)
        return app
    
    @classmethod
    def create_app_db(cls):
        mdb.db.create_all(app=cls.create_app())