from flask_login import login_required
from app import app
from models import Session, Note


@app.route('/notes', methods=['GET'])
@login_required
def get_notes():
    with Session() as session:
        return session.query(Note).all()
