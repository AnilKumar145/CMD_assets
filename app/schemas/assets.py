from pydantic import BaseModel, field_validator
from datetime import date
from typing import List
from enum import Enum
from decimal import Decimal


class Status(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class AssetBase(BaseModel):
    asset_name: str
    value: Decimal
    purchase_date: date
    manufacturer: str
    model: str
    serial_number: str
    supplier: str
    warranty: int 
    warranty_expiry: date
    status: Status = Status.ACTIVE
    facility_name: str

    @field_validator('warranty_expiry')
    def validate_warranty_expiry(cls, v):
        if v < date.today():
            raise ValueError("Warranty expiry must be in the future")
        return v

    @field_validator('warranty')
    def validate_warranty(cls, v):
        if v < 0 or v > 120:
            raise ValueError("Warranty must be between 0 and 120 months")
        return v


class AssetCreate(AssetBase):
    asset_name: str
    value: Decimal
    purchase_date: date
    manufacturer: str
    model: str
    serial_number: str
    supplier: str
    warranty: int
    warranty_expiry: date
    status: Status = Status.ACTIVE
    facility_name: str

    class Config:
        orm_mode = True


class AssetResponse(AssetBase):
    asset_id: str
    value: Decimal
    purchase_date: date
    asset_name: str
    manufacturer: str
    model: str
    serial_number: str
    supplier: str
    warranty: int 
    
    class Config:
        orm_mode = True

class FacilityNamesResponse(BaseModel):
    facility_names: List[str]
