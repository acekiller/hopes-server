from flask import Flask
from database import mdb
from auth import auth
from redis import Redis
import config as config

app = Flask(__name__)
redis_store = Redis(host=config.redis_host, port=config.redis_port, db=0)

class App():
    @classmethod
    def create_app(cls):
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