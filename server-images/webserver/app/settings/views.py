from flask import abort, Blueprint, flash, g, redirect, render_template, \
    url_for
from flask.ext.login import login_required

from app import db
from app.settings.forms import ChangePasswordForm, GeneralSettingsForm
from app.home.views import storage_plan_required
from app.models import StoragePlan
from app.settings.forms import StoragePlanForm

mod = Blueprint('settings', __name__, url_prefix='/settings')


@mod.route('/')
@mod.route('/account')
@login_required
@storage_plan_required
def account():
    user_settings = g.user.settings
    
    g_settings_form = GeneralSettingsForm(timezone=float(user_settings.timezone))
    g_settings_form.new_device_email.data = user_settings.new_device_email
    g_settings_form.almost_out_of_space_email.data = user_settings.almost_out_of_space_email
    g_settings_form.syncsecure_news_email.data = user_settings.syncsecure_news_email

    change_password_form = ChangePasswordForm()

    return render_template("settings/settings-account.html",
                           general_settings_form=g_settings_form,
                           change_password_form=change_password_form)


@mod.route('/storage')
@login_required
@storage_plan_required
def storage():
    show_basic, show_pro, show_pro_plus = 2, 1, 1
    space = g.user.storage_plan.space
    if space == 107374182400:
        show_basic = 1
        show_pro = 3
    if space == 536870912000:
        show_basic = 1
        show_pro_plus = 2
        show_pro = 2

    basic_form = StoragePlanForm()
    pro_form = StoragePlanForm()
    pro_plus_form = StoragePlanForm()

    return render_template("settings/settings-storage.html", show_pro=show_pro,
                           show_pro_plus=show_pro_plus, show_basic=show_basic,
                           basic_form=basic_form, pro_form=pro_form,
                           pro_plus_form=pro_plus_form)


@mod.route('/general/save', methods=["POST"])
@login_required
@storage_plan_required
def save_general_settings():
    g_settings_form = GeneralSettingsForm()
    g.user.settings.new_device_email = g_settings_form.new_device_email.data
    g.user.settings.almost_out_of_space_email = g_settings_form.almost_out_of_space_email.data
    g.user.settings.syncsecure_news_email = g_settings_form.syncsecure_news_email.data
    try:
        g.user.settings.timezone = float(g_settings_form.timezone.data)
    except:
        flash("There was an error setting the timezone.", 'danger')
        return redirect(url_for('settings.account'))
    
    # save the changes to the database
    db.session.commit()
    
    flash("Changes were saved successfully.", 'success')

    return redirect(url_for('settings.account'))


@mod.route('/password/save', methods=["POST"])
@login_required
@storage_plan_required
def save_new_password():
    change_password_form = ChangePasswordForm()

    if change_password_form.validate_on_submit():
        new_password = change_password_form.new_password.data
        if len(new_password) >= 8:
            g.user.set_password(new_password)
            db.session.commit()
            flash("Password was changed successfully.", "success")
        else:
            flash("The password you entered was not long enough.", "warning")
    else:
        flash("The passwords you entered did not match.", "danger")

    return redirect(url_for('settings.account'))


@mod.route('/storage/<plan_name>/save', methods=["POST"])
@login_required
@storage_plan_required
def switch_storage_plan(plan_name):
    usage = g.user.usage.used_space

    form = StoragePlanForm()
    if form.validate_on_submit():
        if plan_name == "basic":
            basic_plan = StoragePlan.query.filter(StoragePlan.id==1).first()
            if usage < basic_plan.space:
                g.user.storage_plan = basic_plan
                g.user.storage_plan_id = 1
                db.session.commit()

                flash("Storage plan switched to basic (10 GB).", "info")
            else:
                flash("Failed to switch plans. Your space usage exceeds 10 GB. Delete some files and try again.", "warning")
        elif plan_name == "pro":
            pro_plan = StoragePlan.query.filter(StoragePlan.id==2).first()
            if usage < pro_plan.space:
                g.user.storage_plan = pro_plan
                g.user.storage_plan_id = 2
                db.session.commit()

                flash("Storage plan switched to pro (100 GB).", "info")
            else:
                flash("Failed to switch plans. Your space usage exceeds 100 GB. Delete some files and try again.", "warning")
        elif plan_name == "pro-plus":
            pro_plus = StoragePlan.query.filter(StoragePlan.id==3).first()
            g.user.storage_plan = pro_plus
            g.user.storage_plan_id = 3
            db.session.commit()

            flash("Storage plan switched to pro plus (500GB).", "info")
        else:
            abort(404)
    else:
        flash("Failed to switch plans.", "danger")
    return redirect(url_for('settings.storage'))
