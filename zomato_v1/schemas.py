from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime, time


class CuisineType(str, Enum):
    INDIAN = "Indian"
    CHINESE = "Chinese"
    ITALIAN = "Italian"


class RestaurantBase(BaseModel):
    id: int
    name: str = Field(..., min_length=3, max_length=100)
    description : Optional[str] = None
    cuisine_type: CuisineType
    address: str = Field(..., min_length=5, max_length=200)
    phone_number: str = Field(..., pattern=r"^\+?[1-9]\d{1,14}$")
    rating: float = Field(default=0.0, ge=0.0, le=5.0)
    is_active: bool = True
    opening_time: time
    closing_time: time
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class RestaurantCreate(RestaurantBase):
    pass

class Restaurant(RestaurantBase):
    class Config:
        orm_mode = True
