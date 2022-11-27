#!/usr/bin/env python3

import uuid
from pickle import dumps, loads
from base64 import b64encode, b64decode
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_login import LoginManager, login_required, current_user
from flask import (Flask, render_template, render_template_string, request,
                   redirect, Response, g, make_response)
from routes import init
from models import RegistrationCode, Session
from utils.notes import get_notes_for_user


def setup_db():
    with Session() as session:
        session.execute(f"DELETE FROM {RegistrationCode.__tablename__}")
        for i in range(100):
            code = RegistrationCode()
            code.code = str(uuid.uuid4())
            session.add(code)

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


@app.route("/")
@login_required
def index():
    return redirect('/home')


@app.route('/home')
@login_required
def home():
    return render_template('home.html',
                           notes=get_notes_for_user(current_user.id))


@app.route('/account')
@login_required
def account():
    return render_template('account.html')


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')


@app.errorhandler(404)
def page_not_found(error):
    detailed_message = render_template_string(
        f"{error}. Requested URL was {request.path}")
    return render_template('404.html', detailed_message=detailed_message)


default_preferences = {'mode': 'light'}


@app.before_request
def before_request():
    preferences = request.cookies.get('preferences')
    if preferences is None:
        preferences = default_preferences
    else:
        preferences = loads(b64decode(preferences))

    g.preferences = preferences


@app.after_request
def after_request(response: Response) -> Response:
    if request.cookies.get('preferences') is None:
        preferences = default_preferences
        response.set_cookie('preferences',
                            b64encode(dumps(preferences)).decode())
    return response


@app.route('/darkmode', methods=['POST'])
def toggle_darkmode():
    response = make_response(redirect('/account'))

    preferences = g.preferences
    preferences['mode'] = 'light' if preferences['mode'] == 'dark' else 'dark'

    response.set_cookie('preferences', b64encode(dumps(preferences)))
    return response
