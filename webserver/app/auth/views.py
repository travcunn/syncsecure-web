from flask import Blueprint, flash, g, redirect, render_template, request, \
    url_for
from flask.ext.login import login_user, logout_user

from app.auth.controllers import LoginValidator
from app.auth.forms import LoginForm

mod = Blueprint('auth', __name__, url_prefix='/auth')


@mod.route('/login', methods=["GET", "POST"])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('home.home'))

    login_form = LoginForm()
    if request.method == "POST":
        if login_form.validate_on_submit():
            login = LoginValidator(email=login_form.email.data,
                                   password=login_form.password.data)

            remember_user = login_form.remember_me.data

            if login.is_valid:
                login_user(login.lookup_user, remember=remember_user)
                return redirect(url_for('home.home'))
            else:
                flash('Incorrect email or password', 'danger')
        else:
            flash("Incorrect email or password", 'danger')

    return render_template('login.html', login_form=login_form)


@mod.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('logged_out.front_page'))
