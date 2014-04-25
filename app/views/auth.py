from flask import flash, g, redirect, request, render_template, url_for
from flask.ext.login import current_user, login_user, logout_user

from app import app, login_manager
from app.controllers import LoginValidator
from app.models import User


login_manager.login_view = 'login'

@app.route('/login', methods=["GET", "POST"])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('admin'))

    if request.method == 'POST':
        #TODO: 
        login = LoginValidator(username=request.form.get('email'),
                               password=request.form.get('password'))
        remember_user = False
        if request.form.get('remember'):
            remember_user = True

        if login.is_valid:
            login_user(login.lookup_user, remember=remember_user)
            flash('You have logged in successfully.', 'success')
            #return redirect(url_for('admin'))
            return redirect(url_for('home'))
        else:
            flash('Incorrect email/password', 'danger')

    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
