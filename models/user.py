from sqlalchemy import Column, String
from .base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, nullable=False)
    password = Column(String)
