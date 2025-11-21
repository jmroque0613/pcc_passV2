# backend/app/routes/auth.py - FIXED VERSION

from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from app.models.user import User
from app.schemas.user_schema import (
    UserRegisterSchema, 
    AdminRegisterSchema,
    UserLoginSchema, 
    TokenSchema, 
    UserResponseSchema,
    PendingUserResponseSchema
)
from app.utils.security import hash_password, verify_password, create_access_token
from app.utils.dependencies import get_current_admin
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegisterSchema):
    """Register a new user - REQUIRES ADMIN APPROVAL"""
    
    # Check if email already exists
    existing_user = await User.find_one(User.email == user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    new_user = User(
        surname=user_data.surname,
        first_name=user_data.first_name,
        middle_name=user_data.middle_name,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
        position=user_data.position,
        salary_grade=user_data.salary_grade,
        starting_date=user_data.starting_date,
        job_category=user_data.job_category,
        assigned_unit=user_data.assigned_unit,
        role="user",
        is_approved=False,  # ⚠️ CRITICAL: Must be False - Requires admin approval!
        is_active=True  # User is active, but not approved yet
    )
    
    await new_user.insert()
    
    return UserResponseSchema(
        id=str(new_user.id),
        surname=new_user.surname,
        first_name=new_user.first_name,
        middle_name=new_user.middle_name,
        email=new_user.email,
        position=new_user.position,
        salary_grade=new_user.salary_grade,
        starting_date=new_user.starting_date,
        job_category=new_user.job_category,
        assigned_unit=new_user.assigned_unit,
        role=new_user.role,
        is_approved=new_user.is_approved,
        is_active=new_user.is_active,
        created_at=new_user.created_at
    )


@router.post("/register-admin", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
async def register_admin(admin_data: AdminRegisterSchema):
    """Register admin user - AUTO APPROVED"""
    
    # Verify admin key
    if admin_data.admin_key != settings.ADMIN_SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid admin key"
        )
    
    # Check if email already exists
    existing_user = await User.find_one(User.email == admin_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create admin user with minimal required fields
    new_admin = User(
        surname="Admin",
        first_name="System",
        middle_name=None,
        email=admin_data.email,
        password_hash=hash_password(admin_data.password),
        position="System Administrator",
        salary_grade="SG 30",
        starting_date=datetime.utcnow(),
        job_category="Regular Employee",
        assigned_unit="Office of the Exec. Director",
        role="admin",
        is_approved=True,  # Admin is auto-approved
        is_active=True
    )
    
    await new_admin.insert()
    
    return UserResponseSchema(
        id=str(new_admin.id),
        surname=new_admin.surname,
        first_name=new_admin.first_name,
        middle_name=new_admin.middle_name,
        email=new_admin.email,
        position=new_admin.position,
        salary_grade=new_admin.salary_grade,
        starting_date=new_admin.starting_date,
        job_category=new_admin.job_category,
        assigned_unit=new_admin.assigned_unit,
        role=new_admin.role,
        is_approved=new_admin.is_approved,
        is_active=new_admin.is_active,
        created_at=new_admin.created_at
    )


@router.post("/login", response_model=TokenSchema)
async def login(login_data: UserLoginSchema):
    """Login endpoint - CHECKS APPROVAL STATUS"""
    
    # Find user by email
    user = await User.find_one(User.email == login_data.email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive. Please contact administrator."
        )
    
    # ⚠️ CHECK APPROVAL STATUS (Only for non-admin users)
    if user.role != "admin" and not user.is_approved:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is pending admin approval. Please wait for approval before logging in."
        )
        
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role}
    )
    
    # Create user response
    user_response = UserResponseSchema(
        id=str(user.id),
        surname=user.surname,
        first_name=user.first_name,
        middle_name=user.middle_name,
        email=user.email,
        position=user.position,
        salary_grade=user.salary_grade,
        starting_date=user.starting_date,
        job_category=user.job_category,
        assigned_unit=user.assigned_unit,
        role=user.role,
        is_approved=user.is_approved,
        is_active=user.is_active,
        created_at=user.created_at
    )
    
    return TokenSchema(
        access_token=access_token,
        user=user_response
    )