from sqlite3 import OperationalError
from sqlalchemy.sql import text

from flask import render_template, request, redirect, flash
from bcrypt import gensalt, hashpw
from app import app
from models import Session, User, RegistrationCode
from forms.registration_form import RegistrationForm


def validate_token(code: str, session: Session) -> str:
    try:
        result = session.execute(
            text(f"""
                SELECT id, code from {RegistrationCode.__tablename__} where code = '{code}'
            """)).first()

        if result is None:
            return False

        return result.id
    except OperationalError as error:
        print(error)
        return False


@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def do_signup():
    form = RegistrationForm(request.form)

    if not form.validate():
        return form.errors

    with Session() as session:
        user_already_exists = session.query(
            session.query(User).where(
                User.email == form.email.data).exists()).scalar()

        code = form.registration_code.data
        if not validate_token(code, session):
            flash("Invalid registration code", 'warning')
            return redirect("/signup")

        if user_already_exists:
            flash("User already exists", 'warning')
            return redirect("/signup")

        user = User()

        user.email = form.email.data
        user.password = hashpw(form.password.data.encode('utf-8'),
                               gensalt()).decode()

        session.add(user)
        session.commit()

    return redirect('/home')
