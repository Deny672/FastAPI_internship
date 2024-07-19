from datetime import datetime, timezone
from sqlalchemy import MetaData, Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import declarative_base

metadata = MetaData()

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    metadata
    id = Column(Integer, primary_key=True)
    first_name = Column(String(40))
    last_name = Column(String(40))
    email = Column(String(60), unique=True, nullable=False, index=True)
    city = Column(String(70))
    phone = Column(String(30))
    avatar = Column(String(255))
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))