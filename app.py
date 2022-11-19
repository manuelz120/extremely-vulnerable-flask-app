#!/usr/bin/env python3

import uuid
from flask_bootstrap import Bootstrap5
from flask import Flask, render_template
from routes import init
from models import RegistrationCode, Session

app = Flask(__name__)
app.secret_key = 'super secret key'
bootstrap = Bootstrap5(app)

init()

with Session() as session:
    session.execute(f"DELETE FROM {RegistrationCode.__tablename__}")
    for i in range(100):
        code = RegistrationCode()
        code.code = str(uuid.uuid4())
        session.add(code)

    session.commit()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/hello/')
def hello():
    return render_template('base.html')
