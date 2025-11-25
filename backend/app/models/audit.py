# backend/app/models/audit.py
from datetime import datetime
from typing import Dict, Optional
from beanie import Document
from pydantic import Field

class AuditLog(Document):
    """Audit log for tracking all system changes"""
    
    # Who performed the action
    user_id: str = Field(..., description="ID of user who performed action")
    user_email: str = Field(..., description="Email of user who performed action")
    user_role: str = Field(..., description="Role of user (admin/user)")
    
    # What action was performed
    action: str = Field(..., description="Action performed: CREATE, UPDATE, DELETE, ASSIGN, UNASSIGN, APPROVE, REJECT")
    
    # What resource was affected
    resource_type: str = Field(..., description="Type of resource: EQUIPMENT, FURNITURE, USER, HR_FILE")
    resource_id: str = Field(..., description="ID of the affected resource")
    resource_name: Optional[str] = Field(None, description="Name/description of resource for easy reference")
    
    # Details of the change
    changes: Dict = Field(default_factory=dict, description="Dictionary of changes made")
    old_values: Optional[Dict] = Field(None, description="Previous values before change")
    new_values: Optional[Dict] = Field(None, description="New values after change")
    
    # Additional context
    ip_address: Optional[str] = Field(None, description="IP address of user")
    user_agent: Optional[str] = Field(None, description="Browser/client information")
    notes: Optional[str] = Field(None, description="Additional notes about the action")
    
    # Timestamp
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="When the action occurred")
    
    class Settings:
        name = "audit_logs"
        indexes = [
            "user_id",
            "action",
            "resource_type",
            "resource_id",
            "timestamp",
            [("resource_type", 1), ("resource_id", 1)],  # Compound index
            [("user_id", 1), ("timestamp", -1)],  # Compound index
        ]
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "user_email": "admin@pcc.gov.ph",
                "user_role": "admin",
                "action": "ASSIGN",
                "resource_type": "EQUIPMENT",
                "resource_id": "507f1f77bcf86cd799439012",
                "resource_name": "Dell Optiplex 7090",
                "changes": {
                    "assigned_to": "John Doe",
                    "status": "Assigned"
                },
                "old_values": {
                    "status": "Available",
                    "assigned_to": None  # ✅ Changed from null to None
                },
                "new_values": {
                    "status": "Assigned",
                    "assigned_to": "John Doe"
                }
            }
        }