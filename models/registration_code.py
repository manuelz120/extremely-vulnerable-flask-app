from sqlalchemy import Column, String
from .base_model import BaseModel


class RegistrationCode(BaseModel):
    __tablename__ = "registration_code"

    def __init__(self, code: str):
        super().__init__()
        self.code = code

    code = Column(String, unique=True, nullable=False)
