#!/usr/bin/env python3

from uuid import uuid4

from flask_login import login_required, current_user
from flask import (render_template, redirect, flash)

from app import app
from models import RegistrationCode, Session


@app.route('/registration-codes', methods=['GET'])
@login_required
def registration_codes():
    if not current_user.is_admin:
        flash("Not authorized to access this page", 'error')
        return redirect('/home')

    with Session() as session:
        codes = session.query(RegistrationCode).all()

        return render_template('registration_codes.html',
                               registration_codes=codes)


@app.route('/registration-codes', methods=['POST'])
@login_required
def add_registration_codes():
    if not current_user.is_admin:
        flash("Not authorized to create new registration codes", 'error')
        return redirect('/home')

    with Session(expire_on_commit=False) as session:
        code = RegistrationCode(str(uuid4()))
        session.add(code)
        session.commit()

    flash(f"Code added: {code.code}", 'success')
    return redirect('/registration-codes')
