from flask import render_template, request
from bcrypt import gensalt, hashpw
from app import app
from models import Session, User
from forms.registration_form import RegistrationForm


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

        if user_already_exists:
            return "User already exists"

        user = User()
        user.email = form.email.data
        user.password = hashpw(form.password.data.encode('utf-8'), gensalt())

        session.add(user)
        session.commit()

    return request.form
