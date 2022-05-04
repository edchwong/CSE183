"""
This file defines the database models
"""
import datetime

from . common import db, Field, auth
from pydal.validators import *

def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
#
# db.commit()
#

db.define_table(
    'contact',
    Field('first_name', requires=IS_NOT_EMPTY()),
    Field('last_name', requires=IS_NOT_EMPTY()),
    Field('created_by', default=get_user_email),
)

db.define_table(
    'numbers',
    Field('phone_number', requires=IS_NOT_EMPTY()),
    Field('phone_type', requires=IS_NOT_EMPTY()),
    Field('contact_id', 'reference contact'),
)

db.numbers.contact_id.writable = False
db.numbers.contact_id.readable = False
db.numbers.id.readable = False
db.numbers.id.writable = False
db.contact.created_by.writable = False
db.contact.created_by.readable = False
db.contact.id.readable = False
db.contact.id.writable = False
db.commit()
