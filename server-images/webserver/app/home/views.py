from functools import wraps

from flask import Blueprint, g, redirect, render_template, url_for
from flask.ext.login import login_required

mod = Blueprint('home', __name__, url_prefix='/home')


def storage_plan_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if g.user is not None and g.user.is_authenticated():
            verification = g.user.verification
            if verification == 'select_plan':
                return redirect(url_for('logged_out.select_storage_plan'))
            elif verification == 'verified':
                return func(*args, **kwargs)
            else:
                return redirect(url_for('logged_out.verify_email'))
        else:
            return func(*args, **kwargs)
    return decorated_view


@mod.route('/')
@login_required
@storage_plan_required
def home():
    return render_template("home/home.html")
