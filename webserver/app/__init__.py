from flask import Flask
from flask.ext.cache import Cache
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from redis import ConnectionPool, Redis

from app.sessions import RedisSessionInterface


app = Flask(__name__)
app.config.from_object('app.config')

cache = Cache(app, config={'CACHE_TYPE': 'redis',
                           'CACHE_REDIS_HOST': '127.0.0.1',
                           'CACHE_KEY_PREFIX': 'appcache.'})

CsrfProtect(app)

login_manager = LoginManager(app)
login_manager.session_protection = "strong"

# REDIS SESSION DATABASE
redis_session_pool = ConnectionPool(host='127.0.0.1', port=6379, db=0)
redis_session = Redis(connection_pool=redis_session_pool)
# set Flask session_interface to the RedisSessionInterface
app.session_interface = RedisSessionInterface(redis=redis_session)

db = SQLAlchemy(app)


from app import views
import filesystem.models
