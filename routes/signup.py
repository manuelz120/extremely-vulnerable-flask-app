from json import dumps
from sqlite3 import OperationalError
from typing import Union
from sqlalchemy.sql import text

from flask import render_template, request, redirect, flash
from bcrypt import gensalt, hashpw
from app import app
from models import Session, User, RegistrationCode
from forms.registration_form import RegistrationForm


def validate_token(code: str, session: Session) -> Union[str, None]:
    try:
        result = session.execute(
            text(f"""
                SELECT id, code FROM {RegistrationCode.__tablename__} WHERE code = '{code}'
            """)).first()

        if result is None:
            return None

        return result.id
    except OperationalError:
        return None


@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def do_signup():
    form = RegistrationForm(request.form)

    if not form.validate():
        flash(dumps(form.errors), 'error')
    else:
        with Session() as session:
            user_already_exists = session.query(
                session.query(User).where(
                    User.email == form.email.data).exists()).scalar()

            code = form.registration_code.data
            token_id = validate_token(code, session)
            if token_id is None:
                flash("Invalid registration code", 'warning')
                return redirect("/signup")

            token = session.get(RegistrationCode, token_id)
            if token.code != code:
                flash("Unexpected registration code mismatch", 'error')
                return redirect("/signup")

            session.delete(token)

            if user_already_exists:
                flash("User already exists", 'warning')
                return redirect("/signup")

            user = User(
                form.email.data,
                hashpw(form.password.data.encode('utf-8'), gensalt()).decode())

            session.add(user)
            session.commit()

    return redirect('/home')
