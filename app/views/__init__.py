from flask import flash, g, redirect, render_template, url_for
from flask.ext.login import login_required

from app import app, db
from app.controllers.forms import GeneralSettingsForm, LoginForm
from app.views import auth


@app.route('/')
def front_page():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('home'))

    login_form = LoginForm()
    return render_template("front-page.html", login_form=login_form)


@app.route('/home')
@login_required
def home():
    return render_template("home.html")


@app.route('/settings')
@app.route('/settings/account')
@login_required
def settings_account():
    user_settings = g.user.settings
    
    g_settings_form = GeneralSettingsForm(timezone=float(user_settings.timezone))
    g_settings_form.new_device_email.data = user_settings.new_device_email
    g_settings_form.almost_out_of_space_email.data = user_settings.almost_out_of_space_email
    g_settings_form.syncsecure_news_email.data = user_settings.syncsecure_news_email

    return render_template("settings-account.html",
                           general_settings_form=g_settings_form)


@app.route('/settings/general/save', methods=["POST"])
@login_required
def save_general_settings():
    g_settings_form = GeneralSettingsForm()
    g.user.settings.new_device_email = g_settings_form.new_device_email.data
    g.user.settings.almost_out_of_space_email = g_settings_form.almost_out_of_space_email.data
    g.user.settings.syncsecure_news_email = g_settings_form.syncsecure_news_email.data
    try:
        g.user.settings.timezone = float(g_settings_form.timezone.data)
    except:
        flash("There was an error setting the timezone.", 'danger')
        return redirect(url_for('settings_account'))
    
    # save the changes to the database
    db.session.commit()
    
    flash("Changes were saved successfully.", 'success')

    return redirect(url_for('settings_account'))



@app.route('/settings/storage')
@login_required
def settings_storage():
    return render_template("settings-storage.html")
