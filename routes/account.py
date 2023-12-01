from pickle import dumps, loads
from base64 import b64encode, b64decode
import json
from uuid import uuid4

from bcrypt import gensalt, hashpw
from flask_login import login_required, current_user
from flask import redirect, flash, render_template, request, Response, g, make_response
from sqlalchemy import text

from app import app
from models import Session, Note
from forms.image_form import ImageForm
from forms.account_form import AccountForm
from utils.profile_image import get_base64_image_blob


@app.route('/account')
@login_required
def account():
    return render_template('account.html', uuid=str(uuid4()))


@app.route('/search')
@login_required
def search():
    search_param = request.args.get('search', '')
    with Session() as session:
        session.query(Note)

        personal_notes = session.query(Note).filter(
            Note.user_id == current_user.id,
            text(f"text like '%{search_param}%'")).all()
        return render_template(
            'search.html',
            search=search_param,
            personal_notes=personal_notes,
        )


@app.route('/accounts/<int:user_id>/notes')
@login_required
def get_personal_notes(user_id: int):
    with Session() as session:
        personal_notes = session.query(Note).filter(
            Note.user_id == user_id).all()
        return render_template('personal_notes.html',
                               personal_notes=personal_notes)


@app.route('/account/image', methods=['POST'])
@login_required
def add_image():
    form = ImageForm(request.form)

    if not form.validate():
        flash(json.dumps(form.errors), 'error')
    else:
        with Session() as session:
            current_user.profile_image = get_base64_image_blob(
                form.url.data).encode()
            session.merge(current_user)
            session.commit()

    return redirect('/account')


@app.route('/account', methods=['POST'])
def update_account():
    form = AccountForm(request.form)

    if not form.validate():
        flash(json.dumps(form.errors), 'error')
    else:
        with Session() as session:
            filtered_values = {
                key: value
                for key, value in form.data.items()
                if value is not None and key != 'password'
            }
            current_user.__dict__.update(filtered_values)

            new_password = form.password.data
            was_password_changed = new_password is not None and new_password != filtered_values.get(
                'password_control')

            if was_password_changed:
                current_user.password = hashpw(new_password.encode(),
                                               gensalt()).decode()

            session.merge(current_user)
            session.commit()
            flash('Account updated', 'success')

    return redirect('/account')


@app.route('/darkmode', methods=['POST'])
def toggle_darkmode():
    response = make_response(redirect('/account'))

    preferences = g.preferences
    preferences['mode'] = 'light' if preferences['mode'] == 'dark' else 'dark'

    response.set_cookie('preferences', b64encode(dumps(preferences)).decode())
    return response


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
