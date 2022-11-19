#!/usr/bin/env python3

from flask_bootstrap import Bootstrap5
from flask import Flask, render_template, request
from forms.registration_form import RegistrationForm
from models import User, Session

app = Flask(__name__)
app.secret_key = 'super secret key'

bootstrap = Bootstrap5(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/hello/')
def hello():
    return render_template('base.html')


@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def do_signup():
    form = RegistrationForm(request.form)
    print(form.data)

    if form.validate():
        with Session() as session:
            user = User()
            user.email = form.email.data
            user.password = form.password.data

            session.add(user)
            session.commit()

        return request.form

    return form.errors
