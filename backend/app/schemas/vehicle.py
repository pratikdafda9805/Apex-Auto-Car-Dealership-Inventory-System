from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class VehicleCreate(BaseModel):
    make: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., min_length=1, max_length=100)
    year: int = Field(..., ge=1900, le=2100)
    category: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    color: Optional[str] = None
    mileage: Optional[int] = Field(None, ge=0)

class VehicleUpdate(BaseModel):
    make: Optional[str] = Field(None, min_length=1, max_length=100)
    model: Optional[str] = Field(None, min_length=1, max_length=100)
    year: Optional[int] = Field(None, ge=1900, le=2100)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)
    color: Optional[str] = None
    mileage: Optional[int] = Field(None, ge=0)

class VehicleResponse(BaseModel):
    id: str
    make: str
    model: str
    year: int
    category: str
    price: float
    quantity: int
    color: Optional[str] = None
    mileage: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class QuantityAction(BaseModel):
    quantity: int = Field(..., gt=0)
