from flask_login import UserMixin
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base_model import BaseModel


class User(BaseModel, UserMixin):
    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False)
    password = Column(String)
    notes = relationship("Note", backref="user")
