from datetime import datetime
from time import time

from sqlalchemy.orm import deferred
from werkzeug.security import generate_password_hash, check_password_hash

from app import cache, db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(96))
    last_name = db.Column(db.String(72))
    email = db.Column(db.String(80), unique=True)
    __password = deferred(db.Column(db.String(96)))

    verification = db.Column(db.String(40))
    creation_date = deferred(db.Column(db.DateTime))

    storage_plan_id = db.Column(db.Integer, db.ForeignKey('storageplan.id'))
    storage_plan = db.relationship('StoragePlan', lazy=True, uselist=False)
    address = db.relationship('Address', lazy=True, uselist=False)
    billing_address = db.relationship('BillingAddress', lazy=True, uselist=False)
    settings = db.relationship('Settings', lazy=True, uselist=False)
    usage = db.relationship('Usage', lazy=True, uselist=False)
    
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)
        self.verification = generate_password_hash(str(time()))[26:]
        self.creation_date = datetime.now()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_verified(self):
        return "x" == self.verification

    def get_id(self):
        return unicode(self.id)

    @cache.memoize(600)
    def get_email(self):
        return self.email

    @cache.memoize(600)
    def get_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @cache.memoize(600)
    def get_first_name(self):
        return self.first_name

    def set_password(self, password):
        """ Sets a new password. """
        self.__password = generate_password_hash(password)

    def check_password(self, password):
        """ Checks a password against the user password """
        return check_password_hash(self.__password, password)

    def __repr__(self):
        return '<User %r>' % (self.email)


class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    country = db.Column(db.String(100))
    address = db.Column(db.String(120))
    zip_code = db.Column(db.String(20))
    city = db.Column(db.String(60))
    state = db.Column(db.String(50))
    phone = db.Column(db.String(50))

    def __init__(self, country, address, zip_code, city, state,
                 phone):
        self.country = country
        self.address = address
        self.zip_code = zip_code
        self.city = city
        self.state = state
        self.phone = phone

    def __repr__(self):
        return '<Address %r>' % (self.user_id)


class BillingAddress(db.Model):
    __tablename__ = 'billingaddress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    country = db.Column(db.String(100))
    address = db.Column(db.String(120))
    zip_code = db.Column(db.String(20))
    city = db.Column(db.String(60))
    state = db.Column(db.String(50))
    phone = db.Column(db.String(50))

    def __init__(self, country, address, zip_code, city, state,
                 phone):
        self.country = country
        self.address = address
        self.zip_code = zip_code
        self.city = city
        self.state = state
        self.phone = phone

    def __repr__(self):
        return '<Address(%r)>' % (self.user_id)


class Settings(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    new_device_email = db.Column(db.Boolean, default=True)
    almost_out_of_space_email = db.Column(db.Boolean, default=True)
    syncsecure_news_email = db.Column(db.Boolean, default=True)
    timezone = db.Column(db.Float, default=-6.0)

    def __repr__(self):
        return '<Settings(%r)>' % (self.user_id)


class Usage(db.Model):
    __tablename__ = 'usage'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    used_space = db.Column(db.Integer, default=0)

    def __init__(self):
        self.used_space = 0

    @cache.memoize(60)
    def gb_used(self):
        return "%.2f" % (float(self.used_space)/pow(1024, 3))

    @cache.memoize(60)
    def percent_used(self):
        user = User.query.filter(User.id==self.user_id).first()
        max_storage = user.storage_plan.space

        percent = (float(self.used_space)/max_storage) * 100
        return "%.2f" % (percent)

    def __repr__(self):
        return "Usage(%r)" % (self.user_id)


class StoragePlan(db.Model):
    __tablename__ = 'storageplan'
    id = db.Column(db.Integer, primary_key=True)
    space = db.Column(db.Integer)  # represented in bytes
    price = db.Column(db.Integer)  # represented in cents

    @cache.memoize(60)
    def to_gb(self):
        return float(self.space)/pow(1024, 3)

    def __repr__(self):
        dollar_amount = float(self.space)/100
        return '<StoragePlan %r bytes for $%r>' % (self.space, dollar_amount)
