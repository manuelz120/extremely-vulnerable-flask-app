from typing import Union
from json import dumps
from flask import render_template, request, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from bcrypt import checkpw
from app import app, login_manager
from models import Session, User
from forms.login_form import LoginForm


@login_manager.user_loader
def load_user(user_id: str) -> Union[User, None]:
    with Session() as session:
        return session.get(User, user_id)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def do_login():
    form = LoginForm(request.form)

    if not form.validate():
        flash(dumps(form.errors), 'error')
    else:
        with Session() as session:
            user = session.query(User).filter(
                User.email == form.email.data).first()
            if user is not None and checkpw(
                    form.password.data.encode('utf-8'),
                    user.password.encode('utf-8')) and login_user(user):
                return redirect("/")

    flash('Invalid Credentials!', 'warning')
    logout_user()

    return redirect("/")


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/is_logged_in', methods=['GET'])
def logged_in():
    return {
        'is_logged_in': current_user.is_authenticated,
        'username':
        current_user.email if current_user.is_authenticated else '-'
    }
