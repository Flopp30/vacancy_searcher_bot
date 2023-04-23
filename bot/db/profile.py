import datetime

from sqlalchemy import Column, Integer, VARCHAR, DATE
from .base import BaseModel

class Profile(BaseModel):
    __tablename__ = "users"

    # telegram user id
    user_id = Column(Integer, unique=True, nullable=False, primary_key=True)

    firstname = Column(VARCHAR(32), nullable=False)
    lastname = Column(VARCHAR(32), nullable=True)

    professional_role = Column(VARCHAR(32), nullable=False)
    experience = Column(VARCHAR(32), nullable=False)

    created_at = Column(DATE, default=datetime.datetime.now())
    updated_at = Column(DATE, onupdate=datetime.datetime.now())

    def __str__(self):
        return f"<User:{self.user_id}>"