from typing import Union
from flask import render_template, request, redirect
from flask_login import login_user, logout_user, current_user
from bcrypt import checkpw
from sqlalchemy import select
from app import app, login_manager
from models import Session, User
from forms.login_form import LoginForm


@login_manager.user_loader
def load_user(user_id: str) -> Union[User, None]:
    print(f"In here: {user_id}")
    with Session() as session:
        return session.get(User, user_id)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def do_login():
    form = LoginForm(request.form)

    if not form.validate():
        return form.errors

    with Session() as session:
        user = session.execute(select(User).order_by(User.id)).fetchone()[0]

        if user is not None and checkpw(form.password.data.encode('utf-8'),
                                        user.password.encode('utf-8')):
            success = login_user(user)
            session.commit()
            return "Yes" if success else "Error"

        logout_user()
        session.commit()
        return "Nope"


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect("")


@app.route('/is_logged_in', methods=['GET'])
def logged_in():
    return {
        'is_logged_in': current_user.is_authenticated,
        'username':
        current_user.email if current_user.is_authenticated else '-'
    }
