from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
from uuid import uuid4
from datetime import datetime

class DBUser(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String, unique=True)
    name = Column(String)
    registered_at = Column(DateTime, default=datetime.utcnow)

class DBEvent(Base):
    __tablename__ = "events"
    event_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    event_type = Column(String)
    payload = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)