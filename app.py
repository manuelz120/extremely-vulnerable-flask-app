#!/usr/bin/env python3

from uuid import uuid4

from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from bcrypt import hashpw, gensalt
from flask import (Flask, render_template, render_template_string, request,
                   redirect)
from routes import init
from models import RegistrationCode, User, Note, Session


def setup_db():
    with Session() as session:
        if session.query(RegistrationCode).count() == 0:
            static_code = 'a36e990b-0024-4d55-b74a-f8d7528e1764'
            session.add(RegistrationCode(static_code))

            for _ in range(10):
                session.add(RegistrationCode(str(uuid4())))
            session.commit()

        if session.query(User).count() == 0:
            user = User('user@evfa.com', hashpw(b'user', gensalt()).decode())
            admin = User('admin@evfa.com',
                         hashpw(b'admin', gensalt()).decode(), True)

            session.add(user)
            session.add(admin)
            session.commit()

            if session.query(Note).count() == 0:
                user_note = Note(id=None,
                                 created_at=None,
                                 title='Shared User Note',
                                 text='A simple note, shared by a normal user',
                                 private=False,
                                 user_id=user.id)
                admin_note = Note(
                    id=None,
                    created_at=None,
                    title='Private admin note',
                    text='A private note, created by an admin user',
                    private=False,
                    user_id=admin.id)

                session.add(user_note)
                session.add(admin_note)
                session.commit()


app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['CKEDITOR_SERVE_LOCAL'] = True
bootstrap = Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)
ckeditor = CKEditor()

ckeditor.init_app(app)
init()
setup_db()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')


@app.errorhandler(404)
def page_not_found(error):
    detailed_message = render_template_string(
        f"{error}. Requested URL was {request.path}")
    return render_template('404.html', detailed_message=detailed_message)
