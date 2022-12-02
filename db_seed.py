from uuid import uuid4
from bcrypt import hashpw, gensalt
from models import RegistrationCode, User, Note, Session


def setup_db():
    with Session() as session:
        if session.query(RegistrationCode).count() == 0:
            static_code = 'a36e990b-0024-4d55-b74a-f8d7528e1764'
            session.add(RegistrationCode(static_code))

            for _ in range(10):
                session.add(RegistrationCode(str(uuid4())))
            session.commit()

        if session.query(User).count() == 0:
            user = User('user@evfa.com', hashpw(b'user', gensalt()).decode())
            admin = User('admin@evfa.com',
                         hashpw(b'admin', gensalt()).decode(), True)

            session.add(user)
            session.add(admin)
            session.commit()

            if session.query(Note).count() == 0:
                user_note = Note(id=None,
                                 created_at=None,
                                 title='Shared User Note',
                                 text='A simple note, shared by a normal user',
                                 private=False,
                                 user_id=user.id)
                admin_note = Note(
                    id=None,
                    created_at=None,
                    title='Private admin note',
                    text='A private note, created by an admin user',
                    private=True,
                    user_id=admin.id)

                session.add(user_note)
                session.add(admin_note)
                session.commit()
