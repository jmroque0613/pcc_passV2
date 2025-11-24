# backend/app/schemas/equipment_schema.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator

# ============ EQUIPMENT SCHEMAS ============

class EquipmentCreateSchema(BaseModel):
    property_number: str = Field(..., min_length=1, max_length=100)
    gsd_code: str = Field(..., min_length=1, max_length=100)
    item_number: str = Field(..., min_length=1, max_length=100)
    equipment_type: str
    brand: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., min_length=1, max_length=100)
    serial_number: str = Field(..., min_length=1, max_length=100)
    specifications: Optional[str] = None
    acquisition_date: datetime
    acquisition_cost: float = Field(..., ge=0)
    condition: str = "New"
    status: str = "Available"
    remarks: Optional[str] = None


class EquipmentUpdateSchema(BaseModel):
    property_number: Optional[str] = None
    gsd_code: Optional[str] = None
    item_number: Optional[str] = None
    equipment_type: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    specifications: Optional[str] = None
    acquisition_date: Optional[datetime] = None
    acquisition_cost: Optional[float] = None
    condition: Optional[str] = None
    status: Optional[str] = None
    remarks: Optional[str] = None


class EquipmentAssignSchema(BaseModel):
    assigned_to_user_id: str
    assigned_to_name: str
    assigned_date: datetime
    assignment_type: str = Field(..., description="PAR or Job Order")
    previous_recipient: Optional[str] = None
    par_number: Optional[str] = None


class EquipmentResponseSchema(BaseModel):
    id: str
    property_number: str
    gsd_code: Optional[str]
    item_number: Optional[str]
    equipment_type: str
    brand: str
    model: str
    serial_number: Optional[str]
    specifications: Optional[str]
    acquisition_date: Optional[datetime]
    acquisition_cost: Optional[float]
    assigned_to_user_id: Optional[str]
    assigned_to_name: Optional[str]
    assigned_date: Optional[datetime]
    assignment_type: Optional[str] = None  # CHANGED: Made optional with default None
    previous_recipient: Optional[str]
    condition: str
    status: str
    remarks: Optional[str]
    par_file_path: Optional[str]
    par_number: Optional[str]
    created_by: str
    created_at: datetime
    updated_at: datetime


# ============ FURNITURE SCHEMAS ============

class FurnitureCreateSchema(BaseModel):
    property_number: str = Field(..., min_length=1, max_length=100)
    gsd_code: str = Field(..., min_length=1, max_length=100)
    item_number: str = Field(..., min_length=1, max_length=100)
    furniture_type: str
    description: str = Field(..., min_length=1, max_length=500)
    brand: Optional[str] = None
    material: Optional[str] = None
    color: Optional[str] = None
    dimensions: Optional[str] = None
    acquisition_date: datetime
    acquisition_cost: float = Field(..., ge=0)
    condition: str = "New"
    status: str = "Available"
    remarks: Optional[str] = None


class FurnitureUpdateSchema(BaseModel):
    property_number: Optional[str] = None
    gsd_code: Optional[str] = None
    item_number: Optional[str] = None
    furniture_type: Optional[str] = None
    description: Optional[str] = None
    brand: Optional[str] = None
    material: Optional[str] = None
    color: Optional[str] = None
    dimensions: Optional[str] = None
    acquisition_date: Optional[datetime] = None
    acquisition_cost: Optional[float] = None
    condition: Optional[str] = None
    status: Optional[str] = None
    remarks: Optional[str] = None
    location: Optional[str] = None


class FurnitureAssignSchema(BaseModel):
    assigned_to_user_id: str
    assigned_to_name: str
    assigned_date: datetime
    assignment_type: str = Field(..., description="PAR or Job Order")
    location: Optional[str] = None
    par_number: Optional[str] = None


class FurnitureResponseSchema(BaseModel):
    id: str
    property_number: str
    gsd_code: Optional[str]
    item_number: Optional[str]
    furniture_type: str
    description: str
    brand: Optional[str]
    material: Optional[str]
    color: Optional[str]
    dimensions: Optional[str]
    acquisition_date: Optional[datetime]
    acquisition_cost: Optional[float]
    assigned_to_user_id: Optional[str]
    assigned_to_name: Optional[str]
    assigned_date: Optional[datetime]
    assignment_type: Optional[str] = None  # CHANGED: Made optional with default None
    location: Optional[str]
    condition: str
    status: str
    remarks: Optional[str]
    par_file_path: Optional[str]
    par_number: Optional[str]
    created_by: str
    created_at: datetime
    updated_at: datetime