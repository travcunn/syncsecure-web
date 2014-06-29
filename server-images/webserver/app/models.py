from datetime import datetime
from time import time

from sqlalchemy.orm import deferred
from werkzeug.security import generate_password_hash, check_password_hash

from app import cache, db


class VirtualFile(db.Model):
    __tablename__ = 'virtualfile'
    id = db.Column(db.Integer, primary_key=True)

    file_share_id = db.Column(db.Integer, db.ForeignKey('fileshare.id'))
    

class VirtualFolder(db.Model):
    __tablename__ = 'virtualfolder'
    id = db.Column(db.Integer, primary_key=True)

    folder_share_id = db.Column(db.Integer, db.ForeignKey('foldershare.id'))
    

class FileShare(db.Model):
    __tablename__ = 'fileshare'
    id = db.Column(db.Integer, primary_key=True)

    # which file does this link to
    share_file_id = db.Column(db.Integer, db.ForeignKey('file.id'))
    # who is this shared with
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # virtual file associated with this file share
    share = db.relationship('VirtualFile', lazy=True, uselist=False)



class FolderShare(db.Model):
    __tablename__ = 'foldershare'
    id = db.Column(db.Integer, primary_key=True)

    # which folder does this link to
    share_folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'))
    # who is this shared with
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # virtual folder associated with this folder share
    share = db.relationship('VirtualFolder', lazy=True, uselist=False)



class File(db.Model):
    __tablename__ = 'file'
    id = db.Column(db.Integer, primary_key=True)
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'))
    
    name = db.Column(db.String(128))
    modified = db.Column(db.DateTime)
    checksum = db.Column(db.String(32))

    shares = db.relationship('FileShare', lazy=True, uselist=True)
    preview = db.relationship('Preview', lazy=True, uselist=False)


class Folder(db.Model):
    __tablename__ = 'folder'
    id = db.Column(db.Integer, primary_key=True)
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'))
    name = db.Column(db.String(128))

    # folder contents
    folder_contents = db.relationship('Folder', lazy=True, uselist=True)
    file_contents = db.relationship('File', lazy=True, uselist=True)
   
    shares = db.relationship('FolderShare', lazy=True, uselist=True)


class Preview(db.Model):
    __tablename__ = 'preview'
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'))


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(96))
    last_name = db.Column(db.String(72))
    email = db.Column(db.String(80), unique=True)
    __password = deferred(db.Column(db.String(96)))
    creation_date = deferred(db.Column(db.DateTime))

    # VERIFICATION INFO
    verification = db.Column(db.String(40))
 
    # STORAGE ROOT FOLDER
    storage_root_id = db.Column(db.Integer, db.ForeignKey('folder.id'))
    storage_root = db.relationship('Folder', lazy=True, uselist=False)

    # STORAGE PLAN
    storage_plan_id = db.Column(db.Integer, db.ForeignKey('storageplan.id'))
    storage_plan = db.relationship('StoragePlan', lazy=True, uselist=False)
    # STORAGE USAGE
    usage = db.relationship('Usage', lazy=True, uselist=False)

    # BILLING INFORMATION
    billing_address = db.relationship('BillingAddress', lazy=True,
                                      uselist=False)
    
    # USER SETTINGS
    settings = db.relationship('Settings', lazy=True, uselist=False)

    # SHARES USER HAS ACCESS TO
    file_shares = db.relationship('FileShare', lazy=True, uselist=True)
    folder_shares = db.relationship('FolderShare', lazy=True, uselist=True)
        
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.set_password(password)
        self.verification = "select_plan"
        self.creation_date = datetime.now()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def create_verification(self):
        self.verification = generate_password_hash(str(time()))[26:]

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

    def __repr__(self):
        return '<BillingAddress(%r)>' % (self.user_id)


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

    @cache.memoize(30)
    def gb_used(self):
        return self.gb_used_no_cache()

    def gb_used_no_cache(self):
        return "%.2f" % (float(self.used_space)/pow(1024, 3))

    @cache.memoize(30)
    def percent_used(self):
        return self.percent_used_no_cache()

    def percent_used_no_cache(self):
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

    @cache.memoize(30)
    def to_gb(self):
        return float(self.space)/pow(1024, 3)

    def __repr__(self):
        dollar_amount = float(self.price)/100
        return '<StoragePlan %r bytes for $%r>' % (self.space, dollar_amount)
