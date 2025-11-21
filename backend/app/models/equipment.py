# backend/app/models/equipment.py
from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import Field

class Equipment(Document):
    # Property Details
    property_number: str  # e.g., "PCC-2024-IT-001"
    gsd_code: str  # GSD Property Code
    item_number: str  # Item tracking number
    
    # Equipment Information
    equipment_type: str  # Desktop, Laptop, Monitor, Printer, Keyboard, Mouse, etc.
    brand: str
    model: str
    serial_number: str
    specifications: Optional[str] = None  # e.g., "Intel i5, 8GB RAM, 256GB SSD"
    
    # Acquisition Details
    acquisition_date: datetime
    acquisition_cost: float
    
    # Assignment Details
    assigned_to_user_id: Optional[str] = None  # Reference to User._id
    assigned_to_name: Optional[str] = None  # Full name for PAR
    assigned_date: Optional[datetime] = None
    previous_recipient: Optional[str] = None
    
    # Condition & Status
    condition: str = "New"  # New, Good, Fair, For Repair, For Disposal
    status: str = "Available"  # Available, Assigned, Under Repair, Disposed
    remarks: Optional[str] = None
    
    # PAR Document
    par_file_path: Optional[str] = None  # Path to uploaded PAR PDF
    par_number: Optional[str] = None  # PAR document number
    
    # Audit Trail
    created_by: str  # Admin email who added this
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "equipment"
        indexes = [
            "property_number",
            "gsd_code",
            "equipment_type",
            "status",
            "assigned_to_user_id",
        ]


class Furniture(Document):
    # Property Details
    property_number: str  # e.g., "PCC-2024-FUR-001"
    gsd_code: str  # GSD Property Code
    item_number: str  # Item tracking number
    
    # Furniture Information
    furniture_type: str  # Office Chair, Desk, Table, Cabinet, Shelf, etc.
    description: str  # Detailed description
    brand: Optional[str] = None
    material: Optional[str] = None  # Wood, Metal, Plastic, etc.
    color: Optional[str] = None
    dimensions: Optional[str] = None  # e.g., "120cm x 60cm x 75cm"
    
    # Acquisition Details
    acquisition_date: datetime
    acquisition_cost: float
    
    # Assignment Details
    assigned_to_user_id: Optional[str] = None  # Reference to User._id
    assigned_to_name: Optional[str] = None  # Full name for PAR
    assigned_date: Optional[datetime] = None
    location: Optional[str] = None  # Office location/room
    
    # Condition & Status
    condition: str = "New"  # New, Good, Fair, For Repair, For Disposal
    status: str = "Available"  # Available, Assigned, Under Repair, Disposed
    remarks: Optional[str] = None
    
    # PAR Document
    par_file_path: Optional[str] = None  # Path to uploaded PAR PDF
    par_number: Optional[str] = None  # PAR document number
    
    # Audit Trail
    created_by: str  # Admin email who added this
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "furniture"
        indexes = [
            "property_number",
            "gsd_code",
            "furniture_type",
            "status",
            "assigned_to_user_id",
        ]


# Enums for dropdown options
EQUIPMENT_TYPES = [
    "Desktop Computer",
    "Laptop",
    "Monitor",
    "Keyboard",
    "Mouse",
    "Printer",
    "Scanner",
    "UPS",
    "External Hard Drive",
    "Network Device",
    "Projector",
    "Webcam",
    "Headset",
    "Other IT Equipment"
]

FURNITURE_TYPES = [
    "Office Chair",
    "Executive Chair",
    "Office Desk",
    "Conference Table",
    "Filing Cabinet",
    "Bookshelf",
    "Storage Cabinet",
    "Drawer",
    "Workstation",
    "Partition",
    "Other Furniture"
]

CONDITIONS = [
    "New",
    "Good",
    "Fair",
    "For Repair",
    "For Disposal"
]

STATUSES = [
    "Available",
    "Assigned",
    "Under Repair",
    "Disposed"
]