import os

DEBUG = True

BASEDIR = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')

RECAPTCHA_PUBLIC_KEY = "6LcIyvISAAAAAIWFtFJJN9Lvag6cfikzlsjniMOe"
RECAPTCHA_PRIVATE_KEY = "6LcIyvISAAAAALKdU7Z5wCAbbmaAHRN5F8Xsc1I-"


# TODO: generate a new SECRET_KEY
SECRET_KEY = '\xfb\x12\xdf\xa1@i\xd6>V\xc0\xbb\x8fp\x16#Z\x0b\x81\xeb\x16'
