from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.models.user import User
from app.schemas.user_schema import UserResponseSchema, PendingUserResponseSchema
from app.utils.dependencies import get_current_admin

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/pending-users", response_model=List[PendingUserResponseSchema])
async def get_pending_users(current_admin: User = Depends(get_current_admin)):
    """Get all users pending approval"""
    pending_users = await User.find(User.is_approved == False).to_list()
    
    return [
        PendingUserResponseSchema(
            id=str(user.id),
            full_name=user.full_name,
            email=user.email,
            position=user.position,
            salary_grade=user.salary_grade,
            job_category=user.job_category,
            assigned_unit=user.assigned_unit,
            created_at=user.created_at
        )
        for user in pending_users
    ]

@router.put("/approve-user/{user_id}", response_model=UserResponseSchema)
async def approve_user(user_id: str, current_admin: User = Depends(get_current_admin)):
    """Approve a pending user"""
    user = await User.get(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.is_approved:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already approved"
        )
    
    user.is_approved = True
    await user.save()
    
    return UserResponseSchema(
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

@router.delete("/reject-user/{user_id}")
async def reject_user(user_id: str, current_admin: User = Depends(get_current_admin)):
    """Reject and delete a pending user"""
    user = await User.get(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    await user.delete()
    return {"message": "User rejected and removed"}

@router.get("/all-users", response_model=List[UserResponseSchema])
async def get_all_users(current_admin: User = Depends(get_current_admin)):
    """Get all users"""
    users = await User.find_all().to_list()
    
    return [
        UserResponseSchema(
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
        for user in users
    ]

@router.put("/deactivate-user/{user_id}")
async def deactivate_user(user_id: str, current_admin: User = Depends(get_current_admin)):
    """Deactivate a user account"""
    user = await User.get(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot deactivate admin accounts"
        )
    
    user.is_active = False
    await user.save()
    
    return {"message": "User deactivated successfully"}