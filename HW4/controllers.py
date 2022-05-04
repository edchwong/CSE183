"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

import uuid

from py4web import action, request, abort, redirect, URL, Field
from py4web.utils.form import Form, FormStyleBulma
from py4web.utils.url_signer import URLSigner
from .models import get_user_email
from yatl.helpers import A
from . common import db, session, T, cache, auth, signed_url, logger, authenticated,unauthenticated, flash


url_signer = URLSigner(session)

# The auth.user below forces login.
@action('index')
@action.uses('index.html', db,session, auth.user,  url_signer)
def index():

    contacts = db(db.contact.created_by == get_user_email()).select()
    rows = db(db.contact.created_by == get_user_email()).select().as_list()
    # and then we iterate on each one, to add the phone numbers for the contact.
    for row in rows:
        # Here we must fish out of the db the phone numbers
        # attached to the contact, and produce a nice string like
        # "354242 (Home), 34343423 (Vacation)" for the contact.
        print(row)
        phones = db(db.numbers.contact_id == row['id']).select().as_list() 
        print(row['id'])
        s = ""
        for phone in phones:
            print(phone)
            s = s + phone['phone_number'] + " (" + phone['phone_type'] + "), "
        print(s)
        # and we can simply assign the nice string to a field of the row! 
        # No matter that the field did not originally exist in the database.
        #row["phone_numbers"] = s
    # So at the end, we can return "nice" rows, each one with our nice string.
    # A row r will have fields r["first_name"], r["last_name"], r["phone_numbers"], ...
    # You can pass these rows to the view, so you can display the table.


    return dict(contacts = contacts,rows=rows, url_signer = url_signer)

## page for adding a new contact
@action('add_contact', method=["GET", "POST"])
@action.uses('add_contact.html', db, session, auth.user)
def add_contact():
    # Insert form: no record= in it.
    form = Form(db.contact, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        # We simply redirect; the insertion already happened.
        redirect(URL('index'))
    # Either this is a GET request, or this is a POST but not accepted = with errors.
    return dict(form=form)




## page for displaying and editing phone_numbers of a contact (the table holding each number)
@action('edit_phones/<contact_id:int>', method=["GET","POST"])
@action.uses('edit_phones.html', db, session, auth.user, url_signer)
def edit_phones(contact_id=None):
    assert contact_id is not None    
    phones = db(db.numbers.contact_id == contact_id).select()

    return dict(phones=phones, url_signer=url_signer)



## page for editing the contact first/last name
@action('edit_contact/<id:int>', method=["GET", "POST"])
@action.uses('edit_contact.html', db, session, auth.user,url_signer.verify())
def edit(id=None):
    assert id is not None
    # We read the bird being edited from the db.
    # p = db(db.bird.id == bird_name).select().first()
    p = db.contact[id]
    if p is None:
        # Nothing found to be edited!
        redirect(URL('index'))
    # Edit form: it has record=
    form = Form(db.contact, record=p, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        # The update already happened!
        redirect(URL('index'))
    return dict(form=form)

## page for adding a phone number in the numbers table
@action('add_phone/<contact_id:int>', method=["GET","POST"])
@action.uses('add_phone.html', db, session, auth.user)
def add_phone(contact_id=None):
    assert contact_id is not None
    form = Form(db.numbers, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        # We simply redirect; the insertion already happened.
        redirect(URL('index'))
    # Either this is a GET request, or this is a POST but not accepted = with errors.
    return dict(form=form)

## page for editing the phone number on the numbers table
@action('edit_phone_number/<contact_id:int>/<numbers_id>', method=["GET", "POST"])
@action.uses('edit_phone_number.html', db, session, auth.user,url_signer.verify())
def edit_phone_number(numbers_id=None):
    assert id is not None
    # We read the bird being edited from the db.
    # p = db(db.bird.id == bird_name).select().first()
    p = db(db.numbers.id == numbers_id).select().first()
    if p is None:
        # Nothing found to be edited!
        redirect(URL('edit_phones'))
    # Edit form: it has record=
    form = Form(db.contact, record=p, csrf_session=session, formstyle=FormStyleBulma)
    if form.accepted:
        # The update already happened!
        redirect(URL('edit_phones'))
    return dict(form=form)

## page for deleting a contact


## page for deleting a number
