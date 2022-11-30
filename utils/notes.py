from typing import List
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from models import Session, Note


def get_notes_for_user(user_id: int) -> List[Note]:
    with Session(expire_on_commit=False) as session:
        return session.query(Note).filter(
            or_(Note.user_id == user_id,
                Note.private == False)).options(joinedload(Note.user)).all()  # pylint: disable=singleton-comparison
