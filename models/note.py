from dataclasses import dataclass
from sqlalchemy import Column, Text, String, Integer, ForeignKey, Boolean
from .base_model import BaseModel


@dataclass
class Note(BaseModel):
    __tablename__ = "notes"
    id: int
    created_at: str
    title: str
    text: str
    user_id: int
    private: bool

    title = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    private = Column(Boolean, default=False)
