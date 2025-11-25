# backend/app/schemas/audit_schema.py
from datetime import datetime
from typing import Dict, Optional
from pydantic import BaseModel

class AuditLogResponseSchema(BaseModel):
    id: str
    user_id: str
    user_email: str
    user_role: str
    action: str
    resource_type: str
    resource_id: str
    resource_name: Optional[str]
    changes: Dict
    old_values: Optional[Dict]
    new_values: Optional[Dict]
    timestamp: datetime