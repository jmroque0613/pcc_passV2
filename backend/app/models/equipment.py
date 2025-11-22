# backend/app/models/equipment.py
from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime

EQUIPMENT_TYPES = [
    "Desktop Computer", "Laptop", "Monitor", "Keyboard", "Mouse",
    "Printer", "Scanner", "UPS", "External Hard Drive", "Network Device",
    "Projector", "Webcam", "Headset", "Other"
]

CONDITIONS = ["Excellent", "Good", "Fair", "Poor", "For Repair"]
STATUSES = ["Available", "Assigned", "Under Repair", "Disposed"]
ASSIGNMENT_TYPES = ["PAR", "Job Order"]  # NEW

class Equipment(Document):
    # Basic Information
    property_number: str = Field(..., description="Property number")
    gsd_code: Optional[str] = Field(None, description="GSD code")
    item_number: Optional[str] = Field(None, description="Item number")
    
    # Equipment Details
    equipment_type: str = Field(..., description="Type of equipment")
    brand: str = Field(..., description="Brand")
    model: str = Field(..., description="Model")
    serial_number: Optional[str] = Field(None, description="Serial number")
    specifications: Optional[str] = Field(None, description="Specifications")
    
    # Acquisition
    acquisition_date: Optional[datetime] = Field(None, description="Date of acquisition")
    acquisition_cost: Optional[float] = Field(None, description="Acquisition cost")
    
    # Assignment Information
    assigned_to_user_id: Optional[str] = Field(None, description="User ID assigned to")
    assigned_to_name: Optional[str] = Field(None, description="Name of person assigned to")
    assigned_date: Optional[datetime] = Field(None, description="Date assigned")
    assignment_type: Optional[str] = Field(None, description="PAR or Job Order")  # NEW
    previous_recipient: Optional[str] = Field(None, description="Previous recipient")
    
    # Status
    condition: str = Field(default="Good", description="Equipment condition")
    status: str = Field(default="Available", description="Equipment status")
    remarks: Optional[str] = Field(None, description="Additional remarks")
    
    # PAR Document
    par_file_path: Optional[str] = Field(None, description="Path to PAR document")
    par_number: Optional[str] = Field(None, description="PAR number")
    
    # Audit
    created_by: str = Field(..., description="Created by user email")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "equipment"


class Furniture(Document):
    # Basic Information
    property_number: str = Field(..., description="Property number")
    gsd_code: Optional[str] = Field(None, description="GSD code")
    item_number: Optional[str] = Field(None, description="Item number")
    
    # Furniture Details
    furniture_type: str = Field(..., description="Type of furniture")
    description: str = Field(..., description="Description")
    brand: Optional[str] = Field(None, description="Brand")
    material: Optional[str] = Field(None, description="Material")
    color: Optional[str] = Field(None, description="Color")
    dimensions: Optional[str] = Field(None, description="Dimensions")
    
    # Acquisition
    acquisition_date: Optional[datetime] = Field(None, description="Date of acquisition")
    acquisition_cost: Optional[float] = Field(None, description="Acquisition cost")
    
    # Assignment Information
    assigned_to_user_id: Optional[str] = Field(None, description="User ID assigned to")
    assigned_to_name: Optional[str] = Field(None, description="Name of person assigned to")
    assigned_date: Optional[datetime] = Field(None, description="Date assigned")
    assignment_type: Optional[str] = Field(None, description="PAR or Job Order")  # NEW
    location: Optional[str] = Field(None, description="Current location")
    
    # Status
    condition: str = Field(default="Good", description="Furniture condition")
    status: str = Field(default="Available", description="Furniture status")
    remarks: Optional[str] = Field(None, description="Additional remarks")
    
    # PAR Document
    par_file_path: Optional[str] = Field(None, description="Path to PAR document")
    par_number: Optional[str] = Field(None, description="PAR number")
    
    # Audit
    created_by: str = Field(..., description="Created by user email")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "furniture"

FURNITURE_TYPES = [
    "Office Chair", "Executive Chair", "Office Desk", "Conference Table",
    "Filing Cabinet", "Bookshelf", "Storage Cabinet", "Drawer",
    "Workstation", "Partition", "Other"
]