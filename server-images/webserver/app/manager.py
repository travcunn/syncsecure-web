from app import db
from app.models import BillingAddress, Folder, Settings, StoragePlan, Usage, \
        User


def create_new_user(first_name, last_name, email, password):
    """ Creates a new user and sets up any links database entries. """
    
    new_user = User(first_name, last_name, email, password)
    db.session.add(new_user)
    db.session.commit()
 
    # link a root storage folder to the user
    root_folder = Folder()
    db.session.add(root_folder)
    db.session.commit()
    new_user.storage_root_id = root_folder.id
    new_user.storage_root = root_folder
    db.session.commit()

    # link usage tracking to the user
    usage = Usage()
    usage.user_id = new_user.id
    new_user.usage = usage
    db.session.add(usage)
    db.session.commit()

    # link a billing address to the user
    billing_address = BillingAddress()
    billing_address.user_id = new_user.id
    new_user.billing_address = billing_address
    db.session.add(billing_address)
    db.session.commit()

    # link settings to the User
    settings = Settings()
    settings.user_id = new_user.id
    new_user.settings = settings
    db.session.add(settings)
    db.session.commit()


def update_storage_plan(user, storage_plan):
    """ Updates the storage plan for a given user. """
    plans = StoragePlan.query
    storage_plan = plans.filter(StoragePlan.id == storage_plan).first()
    user.storage_plan_id = storage_plan.id
    user.storage_plan = storage_plan
    db.session.commit()


def delete_user(user):
    """ Deletes a user. """
    settings = user.settings
    db.session.delete(settings)

    usage = user.usage
    db.session.delete(usage)

    billing_address = user.billing_address
    db.session.delete(billing_address)

    db.session.commit()


def delete_user_files(user):
    pass
