from app import db
from app.models import User


class LoginValidator(object):
    def __init__(self, email, password):
        self.__email = email
        self.__password = password

    @property
    def is_valid(self):
        user = self.lookup_user
        if user is None:
            return False

        if not user.check_password(self.__password):
            return False

        return True

    @property
    def lookup_user(self):
        return db.session.query(User).filter_by(email=self.__email).first()
