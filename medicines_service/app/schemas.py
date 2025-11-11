from sqlalchemy import Column, String, Float, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from .database import Base
from uuid import uuid4
from datetime import datetime

class DBMedicine(Base):
    __tablename__ = "medicine_catalog"
    medicine_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)
    updated_at = Column(DateTime, default=datetime.utcnow)