from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator

class UserRegisterSchema(BaseModel):
    # Personal Information
    surname: str = Field(..., min_length=1, max_length=100)
    first_name: str = Field(..., min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    
    # Login Credentials
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    
    # Employment Details
    position: str = Field(..., min_length=1, max_length=200)
    salary_grade: str
    starting_date: datetime
    job_category: str
    assigned_unit: str
    
    @validator('salary_grade')
    def validate_salary_grade(cls, v):
        valid_grades = [f"SG {i}" for i in range(1, 31)]
        if v not in valid_grades:
            raise ValueError('Invalid salary grade. Must be SG 1 to SG 30')
        return v
    
    @validator('job_category')
    def validate_job_category(cls, v):
        valid_categories = ["Job Order", "Regular Employee"]
        if v not in valid_categories:
            raise ValueError('Invalid job category')
        return v
    
    @validator('assigned_unit')
    def validate_assigned_unit(cls, v):
        valid_units = ["CCRD", "CCTSIRMD", "ISSU", "Office of the Exec. Director"]
        if v not in valid_units:
            raise ValueError('Invalid assigned unit')
        return v


class AdminRegisterSchema(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    admin_key: str = Field(..., min_length=1)


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    id: str
    surname: str
    first_name: str
    middle_name: Optional[str]
    email: str
    position: str
    salary_grade: str
    starting_date: datetime
    job_category: str
    assigned_unit: str
    role: str
    is_approved: bool
    is_active: bool
    created_at: datetime
    
    @property
    def full_name(self) -> str:
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.surname}"
        return f"{self.first_name} {self.surname}"


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponseSchema


class PendingUserResponseSchema(BaseModel):
    id: str
    full_name: str
    email: str
    position: str
    salary_grade: str
    job_category: str
    assigned_unit: str
    created_at: datetime