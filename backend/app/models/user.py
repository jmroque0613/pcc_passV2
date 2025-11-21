from datetime import datetime
from typing import Optional
from beanie import Document
from pydantic import EmailStr, Field

class User(Document):
    # Personal Information
    surname: str
    first_name: str
    middle_name: Optional[str] = None
    
    # Login Credentials
    email: EmailStr
    password_hash: str
    
    # Employment Details
    position: str
    salary_grade: str  # SG 1 - SG 30
    starting_date: datetime
    job_category: str  # "Job Order" or "Regular Employee"
    assigned_unit: str  # CCRD, CCTSIRMD, ISSU, Office of the Exec. Director
    
    # User Status
    role: str = "user"  # "user" or "admin"
    is_approved: bool = False  # Admin must approve registration
    is_active: bool = True
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "users"
        indexes = [
            "email",
            "is_approved",
            "role",
        ]
    
    @property
    def full_name(self) -> str:
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.surname}"
        return f"{self.first_name} {self.surname}"