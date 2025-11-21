# backend/app/schemas/equipment_schema.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator

# ============ EQUIPMENT SCHEMAS ============

class EquipmentCreateSchema(BaseModel):
    # Property Details
    property_number: str = Field(..., min_length=1, max_length=100)
    gsd_code: str = Field(..., min_length=1, max_length=100)
    item_number: str = Field(..., min_length=1, max_length=100)
    
    # Equipment Information
    equipment_type: str
    brand: str = Field(..., min_length=1, max_length=100)
    model: str = Field(..., min_length=1, max_length=100)
    serial_number: str = Field(..., min_length=1, max_length=100)
    specifications: Optional[str] = None
    
    # Acquisition Details
    acquisition_date: datetime
    acquisition_cost: float = Field(..., ge=0)
    
    # Condition & Status
    condition: str = "New"
    status: str = "Available"
    remarks: Optional[str] = None
    
    @validator('equipment_type')
    def validate_equipment_type(cls, v):
        valid_types = [
            "Desktop Computer", "Laptop", "Monitor", "Keyboard", "Mouse",
            "Printer", "Scanner", "UPS", "External Hard Drive", "Network Device",
            "Projector", "Webcam", "Headset", "Other IT Equipment"
        ]
        if v not in valid_types:
            raise ValueError(f'Invalid equipment type. Must be one of: {", ".join(valid_types)}')
        return v
    
    @validator('condition')
    def validate_condition(cls, v):
        valid_conditions = ["New", "Good", "Fair", "For Repair", "For Disposal"]
        if v not in valid_conditions:
            raise ValueError(f'Invalid condition. Must be one of: {", ".join(valid_conditions)}')
        return v
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ["Available", "Assigned", "Under Repair", "Disposed"]
        if v not in valid_statuses:
            raise ValueError(f'Invalid status. Must be one of: {", ".join(valid_statuses)}')
        return v


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
    previous_recipient: Optional[str] = None
    par_number: Optional[str] = None


class EquipmentResponseSchema(BaseModel):
    id: str
    property_number: str
    gsd_code: str
    item_number: str
    equipment_type: str
    brand: str
    model: str
    serial_number: str
    specifications: Optional[str]
    acquisition_date: datetime
    acquisition_cost: float
    assigned_to_user_id: Optional[str]
    assigned_to_name: Optional[str]
    assigned_date: Optional[datetime]
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
    # Property Details
    property_number: str = Field(..., min_length=1, max_length=100)
    gsd_code: str = Field(..., min_length=1, max_length=100)
    item_number: str = Field(..., min_length=1, max_length=100)
    
    # Furniture Information
    furniture_type: str
    description: str = Field(..., min_length=1, max_length=500)
    brand: Optional[str] = None
    material: Optional[str] = None
    color: Optional[str] = None
    dimensions: Optional[str] = None
    
    # Acquisition Details
    acquisition_date: datetime
    acquisition_cost: float = Field(..., ge=0)
    
    # Condition & Status
    condition: str = "New"
    status: str = "Available"
    remarks: Optional[str] = None
    
    @validator('furniture_type')
    def validate_furniture_type(cls, v):
        valid_types = [
            "Office Chair", "Executive Chair", "Office Desk", "Conference Table",
            "Filing Cabinet", "Bookshelf", "Storage Cabinet", "Drawer",
            "Workstation", "Partition", "Other Furniture"
        ]
        if v not in valid_types:
            raise ValueError(f'Invalid furniture type. Must be one of: {", ".join(valid_types)}')
        return v


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
    location: Optional[str] = None
    par_number: Optional[str] = None


class FurnitureResponseSchema(BaseModel):
    id: str
    property_number: str
    gsd_code: str
    item_number: str
    furniture_type: str
    description: str
    brand: Optional[str]
    material: Optional[str]
    color: Optional[str]
    dimensions: Optional[str]
    acquisition_date: datetime
    acquisition_cost: float
    assigned_to_user_id: Optional[str]
    assigned_to_name: Optional[str]
    assigned_date: Optional[datetime]
    location: Optional[str]
    condition: str
    status: str
    remarks: Optional[str]
    par_file_path: Optional[str]
    par_number: Optional[str]
    created_by: str
    created_at: datetime
    updated_at: datetime