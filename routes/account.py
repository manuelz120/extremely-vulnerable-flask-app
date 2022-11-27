from pickle import dumps, loads
from base64 import b64encode, b64decode

from flask_login import login_required, current_user
from flask import redirect, flash, render_template, request, Response, g, make_response

from app import app
from models import Session, Note
from forms.image_form import ImageForm
from utils.profile_image import get_base64_image_blob


@app.route('/account')
@login_required
def account():
    return render_template('account.html')


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
        flash(dumps(form.errors), 'error')

    with Session() as session:
        current_user.profile_image = get_base64_image_blob(
            form.url.data).encode()
        session.merge(current_user)
        session.commit()

    return redirect('/account')


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
