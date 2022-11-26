from sqlalchemy import Column, Text, Integer, ForeignKey, Boolean
from .base_model import BaseModel


class Note(BaseModel):
    __tablename__ = "notes"

    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    private = Column(Boolean, default=False)
