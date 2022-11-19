from sqlalchemy import Column, String
from .base_model import BaseModel


class RegistrationCode(BaseModel):
    __tablename__ = "registration_code"

    code = Column(String, unique=True, nullable=False)
