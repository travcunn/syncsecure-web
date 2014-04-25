from werkzeug.security import generate_password_hash, check_password_hash

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(96))
    last_name = db.Column(db.String(72))
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(96))

    verified = db.Column(db.Boolean, default=False)
    creation_date = db.Column(db.DateTime)
    address = db.relationship('Address',
                backref=db.backref('user', lazy='joined'), lazy='dynamic',
                uselist=False)
    billing_address = db.relationship('Address',
                backref=db.backref('user', lazy='joined'), lazy='dynamic',
                uselist=False)

    def __init__(self, first_name, last_name, email, password, creation_date):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)
        self.verified = False
        self.creation_date = creation_date

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def set_password(self, password):
        """ Sets a new password. """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """ Checks a password against the user password """
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % (self.email)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    country = db.Column(db.String(100))
    address = db.Column(db.String(120))
    zip_code = db.Column(db.String(20))
    city = db.Column(db.String(60))
    state = db.Column(db.String(50))
    phone = db.Column(db.String(50))

    def __init__(self, user_id, country, address, zip_code, city, state,
                 phone):
        self.user_id = user_id
        self.country = country
        self.address = address
        self.zip_code = zip_code
        self.city = city
        self.state = state
        self.phone = phone

    def __repr__(self):
        return '<Address %r>' % (self.country)
