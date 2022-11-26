#!/usr/bin/env python3

import uuid
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, login_required
from flask import Flask, render_template, render_template_string, request, redirect
from routes import init
from models import RegistrationCode, Session

app = Flask(__name__)
app.secret_key = 'super secret key'
bootstrap = Bootstrap5(app)
login_manager = LoginManager()
login_manager.init_app(app)

init()

with Session() as session:
    session.execute(f"DELETE FROM {RegistrationCode.__tablename__}")
    for i in range(100):
        code = RegistrationCode()
        code.code = str(uuid.uuid4())
        session.add(code)

    session.commit()


@app.route("/")
@login_required
def index():
    return redirect('/home')


@app.route('/home')
@login_required
def home():
    return render_template('home.html')


@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')


@app.errorhandler(404)
def page_not_found(error):
    detailed_message = render_template_string(
        f"{error}. Requested URL was {request.path}")
    return render_template('404.html', detailed_message=detailed_message)
