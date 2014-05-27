from flask import Blueprint, flash, g, redirect, render_template, request, \
    url_for
from flask.ext.login import login_required

from app import db
from app.auth.forms import LoginForm
from app.logged_out.forms import ResendVerifyEmailForm
from app.models import StoragePlan
from app.settings.forms import StoragePlanForm


mod = Blueprint('logged_out', __name__)


@mod.route('/')
def front_page():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('home.home'))

    print "Hello"
    login_form = LoginForm()
    return render_template("front-page.html", login_form=login_form)


@mod.route('/verify-email', methods=["GET"])
@login_required
def verify_email():
    print "verify"
    if g.user is not None and g.user.is_authenticated():
        if g.user.verification == 'verified':
            return redirect(url_for('home.home'))

    resend_form = ResendVerifyEmailForm()
    return render_template("verify-email.html", resend_form=resend_form)


@mod.route('/verify-email/resend', methods=["POST"])
@login_required
def resend_verification():
    return "Resending shit"


@mod.route('/select-storage-plan', methods=["GET"])
@login_required
def select_storage_plan():
    if g.user is not None and g.user.is_authenticated():
        if g.user.verification != 'select_plan':
            return redirect(url_for('home.home'))

    basic_form = StoragePlanForm()
    pro_form = StoragePlanForm()
    pro_plus_form = StoragePlanForm()

    return render_template("select-storage-plan.html", basic_form=basic_form,
                           pro_form=pro_form, pro_plus_form=pro_plus_form)


@mod.route('/select-storage-plan/<plan_name>', methods=["POST"])
@login_required
def save_storage_plan(plan_name):
    if g.user is not None and g.user.is_authenticated():
        if g.user.verification != 'select_plan':
            return redirect(url_for('home.home'))

    form = StoragePlanForm()
    sp = StoragePlan

    if request.method == "POST":
        if form.validate_on_submit():
            if plan_name == "basic":
                basic_plan = sp.query.filter(sp.id==1).first()
                g.user.storage_plan = basic_plan
                g.user.storage_plan_id = 1
                
                g.user.create_verification()
                db.session.commit()
                return redirect(url_for('logged_out.verify_email'))
            elif plan_name == "pro":
                pro_plan = sp.query.filter(sp.id==2).first()
                g.user.storage_plan = pro_plan
                g.user.storage_plan_id = 2

                g.user.create_verification()
                db.session.commit()
                return redirect(url_for('logged_out.verify_email'))
            elif plan_name == "pro-plus":
                pro_plus_plan = sp.query.filter(sp.id==3).first()
                g.user.storage_plan = pro_plus_plan
                g.user.storage_plan_id = 3

                g.user.create_verification()
                db.session.commit()
                return redirect(url_for('logged_out.verify_email'))
            else:
                flash("There was an error selecting a plan.", "danger")
        else:
            flash("There was an error selecting a plan.", "danger")

    return redirect(url_for('logged_out.select_storage_plan'))

