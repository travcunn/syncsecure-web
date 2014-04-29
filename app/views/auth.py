from flask import flash, g, redirect, request, render_template, url_for
from flask.ext.login import current_user, login_user, logout_user

from app import app, login_manager
from app.controllers import LoginValidator
from app.controllers.forms import LoginForm
from app.models import User


login_manager.login_view = 'login'


@app.route('/login', methods=["GET", "POST"])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('home'))

    login_form = LoginForm()
    if request.method == "POST":
        if login_form.validate_on_submit():
            login = LoginValidator(email=login_form.email.data,
                                   password=login_form.password.data)

            remember_user = login_form.remember_me.data

            if login.is_valid:
                login_user(login.lookup_user, remember=remember_user)
                return redirect(url_for('home'))
            else:
                flash('Incorrect email or password', 'danger')
        else:
            flash("Incorrect email or password", 'danger')

    return render_template('login.html', login_form=login_form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('front_page'))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
