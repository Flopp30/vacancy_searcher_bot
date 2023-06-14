"""
BaseModel sql alchemy
"""
import datetime

from sqlalchemy import Column, DATE, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


class CustomBaseModel(BaseModel):
    __abstract__ = True

    id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    created_at = Column(DATE, default=datetime.datetime.now())
    updated_at = Column(DATE, onupdate=datetime.datetime.now())

    is_deleted = Column(Boolean, default=False)
