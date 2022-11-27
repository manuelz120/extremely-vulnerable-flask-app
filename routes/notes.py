from flask_login import login_required, current_user
from flask import request, redirect, flash
from app import app
from forms.note_form import NoteForm
from models import Session, Note
from utils.notes import get_notes_for_user


@app.route('/notes', methods=['GET'])
@login_required
def get_notes():
    return get_notes_for_user(current_user.id)


@app.route('/notes', methods=['POST'])
@login_required
def add_note():
    form = NoteForm(request.form)

    if not form.validate():
        return form.errors

    with Session(expire_on_commit=False) as session:
        note = Note()
        note.title = form.title.data
        note.text = form.text.data
        note.private = form.private.data
        note.user_id = current_user.id
        session.add(note)
        session.commit()

    flash('Note created', 'success')
    return redirect('/home')
