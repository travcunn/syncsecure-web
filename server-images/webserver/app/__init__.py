from flask import Flask
from flask.ext.cache import Cache
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from raven.contrib.flask import Sentry
from redis import ConnectionPool, Redis

from app.sessions import RedisSessionInterface


app = Flask(__name__)
app.config.from_object('app.config')

sentry = Sentry(app)

if not app.debug:
    import etcd

    client = etcd.Client()
    redis_cache_ip = client.read('/nodes/redis-cache').value
    redis_sessions_ip = client.read('/nodes/redis-sessions').value

    # REDIS SESSION DATABASE
    redis_session_pool = ConnectionPool(host=redis_sessions_ip, port=6379,
                                        db=0)
    redis_session = Redis(connection_pool=redis_session_pool)
    # set Flask session_interface to the RedisSessionInterface
    app.session_interface = RedisSessionInterface(redis=redis_session)

    cache = Cache(app, config={'CACHE_TYPE': 'redis',
                               'CACHE_REDIS_HOST': redis_cache_ip,
                               'CACHE_KEY_PREFIX': 'appcache.'}) 

else:
    cache = Cache(app, config={'CACHE_TYPE': 'simple'})
    
CsrfProtect(app)

login_manager = LoginManager(app)
login_manager.session_protection = "strong"
    
db = SQLAlchemy(app)


from app import views
import filesystem.models
