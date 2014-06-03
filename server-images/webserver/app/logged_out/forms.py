from flask_wtf import Form, RecaptchaField


class ResendVerifyEmailForm(Form):
    recaptcha = RecaptchaField()
