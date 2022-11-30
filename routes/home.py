from flask import render_template, redirect
from flask_login import login_required, current_user

from app import app
from utils.notes import get_notes_for_user


@app.route("/")
@login_required
def index():
    return redirect('/home')


@app.route('/home')
@login_required
def home():
    return render_template('home.html',
                           notes=get_notes_for_user(current_user.id))
