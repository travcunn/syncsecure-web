from flask import render_template
from flask.ext.login import login_required

from app import app
from app.views import auth


@app.route('/')
def front_page():
    return render_template("front-page.html")


@app.route('/home')
def home():
    return render_template("home.html")

"""
@app.route('/home')
@login_required
def protected_view():
    return "secret logged in area"
"""
