from typing import List
from sqlalchemy import or_
from models import Session, Note


def get_notes_for_user(user_id: int) -> List[Note]:
    with Session() as session:
        return session.query(Note).filter(
            or_(Note.user_id == user_id, Note.private is False)).all()
