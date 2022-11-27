from json import dumps
from flask_login import login_required, current_user
from flask import request, redirect, flash
from app import app
from forms.image_form import ImageForm
from models import Session
from utils.profile_image import get_base64_image_blob


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
