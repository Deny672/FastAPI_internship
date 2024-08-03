from datetime import datetime
from sqlalchemy import MetaData, Column, Integer, String, DateTime, Boolean, func
from sqlalchemy.orm import declarative_base

metadata = MetaData()

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    metadata
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(40), nullable=True)
    last_name = Column(String(40), nullable=True)
    email = Column(String(60), unique=True, nullable=False)
    city = Column(String(70), nullable=True)
    phone = Column(String(30), nullable=True)
    avatar = Column(String(255), nullable=True)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)