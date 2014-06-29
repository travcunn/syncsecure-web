from flask import g
from flask.ext.login import current_user

from app import app, login_manager
from app.api.views import mod as apiModule
from app.auth.views import mod as authModule
from app.home.views import mod as homeModule
from app.logged_out.views import mod as loggedOutModule
from app.models import User
from app.settings.views import mod as settingsModule

login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user


app.register_blueprint(apiModule)
app.register_blueprint(authModule)
app.register_blueprint(homeModule)
app.register_blueprint(loggedOutModule)
app.register_blueprint(settingsModule)
