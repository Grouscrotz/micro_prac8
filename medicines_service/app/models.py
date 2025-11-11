from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Optional
from uuid import UUID

class Medicine(BaseModel):
    medicine_id: Optional[UUID] = None
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True
    updated_at: Optional[datetime] = None

    # ВАЖНО: Pydantic V2
    model_config = ConfigDict(from_attributes=True)

    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Цена не может быть отрицательной')
        return v