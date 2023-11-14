from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    String,
    Integer,
)


BASE = declarative_base()

class User(BASE):
    """a model for the user"""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(300), unique=True, nullable=False)
    password = Column(String(300), nullable=False)
    username = Column(String(300), nullable=False)
    phone_number = Column(String(300), nullable=True)
    address = Column(String(500), nullable=True)
