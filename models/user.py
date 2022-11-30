from flask_login import UserMixin
from sqlalchemy import Column, String, BLOB, Boolean
from sqlalchemy.orm import relationship
from .base_model import BaseModel


class User(BaseModel, UserMixin):
    __tablename__ = "users"

    def __init__(self, email: str, password: str, is_admin: bool = False):
        super().__init__()
        self.email = email
        self.password = password
        self.is_admin = is_admin

    email = Column(String, unique=True, nullable=False)
    password = Column(String)
    notes = relationship("Note", backref="user")
    profile_image = Column(BLOB)
    is_admin = Column(Boolean, default=False)
