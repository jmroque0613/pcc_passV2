# backend/app/routes/furniture.py
from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from fastapi.responses import FileResponse
import aiofiles
import os

from app.models.user import User
from app.models.equipment import Furniture, FURNITURE_TYPES, CONDITIONS, STATUSES
from app.schemas.equipment_schema import (
    FurnitureCreateSchema,
    FurnitureUpdateSchema,
    FurnitureAssignSchema,
    FurnitureResponseSchema
)
from app.utils.dependencies import get_current_admin, get_current_user

router = APIRouter(prefix="/api/furniture", tags=["Furniture"])

# ============ ADMIN ROUTES ============

@router.post("/", response_model=FurnitureResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_furniture(
    furniture_data: FurnitureCreateSchema,
    current_admin: User = Depends(get_current_admin)
):
    """Create new furniture - Admin only"""
    
    # Check if property number already exists
    existing = await Furniture.find_one(Furniture.property_number == furniture_data.property_number)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Property number already exists"
        )
    
    # Create furniture
    new_furniture = Furniture(
        property_number=furniture_data.property_number,
        gsd_code=furniture_data.gsd_code,
        item_number=furniture_data.item_number,
        furniture_type=furniture_data.furniture_type,
        description=furniture_data.description,
        brand=furniture_data.brand,
        material=furniture_data.material,
        color=furniture_data.color,
        dimensions=furniture_data.dimensions,
        acquisition_date=furniture_data.acquisition_date,
        acquisition_cost=furniture_data.acquisition_cost,
        condition=furniture_data.condition,
        status=furniture_data.status,
        remarks=furniture_data.remarks,
        created_by=current_admin.email
    )
    
    await new_furniture.insert()
    
    return FurnitureResponseSchema(
        id=str(new_furniture.id),
        property_number=new_furniture.property_number,
        gsd_code=new_furniture.gsd_code,
        item_number=new_furniture.item_number,
        furniture_type=new_furniture.furniture_type,
        description=new_furniture.description,
        brand=new_furniture.brand,
        material=new_furniture.material,
        color=new_furniture.color,
        dimensions=new_furniture.dimensions,
        acquisition_date=new_furniture.acquisition_date,
        acquisition_cost=new_furniture.acquisition_cost,
        assigned_to_user_id=new_furniture.assigned_to_user_id,
        assigned_to_name=new_furniture.assigned_to_name,
        assigned_date=new_furniture.assigned_date,
        location=new_furniture.location,
        condition=new_furniture.condition,
        status=new_furniture.status,
        remarks=new_furniture.remarks,
        par_file_path=new_furniture.par_file_path,
        par_number=new_furniture.par_number,
        created_by=new_furniture.created_by,
        created_at=new_furniture.created_at,
        updated_at=new_furniture.updated_at
    )


@router.get("/", response_model=List[FurnitureResponseSchema])
async def get_all_furniture(current_admin: User = Depends(get_current_admin)):
    """Get all furniture - Admin only"""
    furniture_list = await Furniture.find_all().to_list()
    
    return [
        FurnitureResponseSchema(
            id=str(fur.id),
            property_number=fur.property_number,
            gsd_code=fur.gsd_code,
            item_number=fur.item_number,
            furniture_type=fur.furniture_type,
            description=fur.description,
            brand=fur.brand,
            material=fur.material,
            color=fur.color,
            dimensions=fur.dimensions,
            acquisition_date=fur.acquisition_date,
            acquisition_cost=fur.acquisition_cost,
            assigned_to_user_id=fur.assigned_to_user_id,
            assigned_to_name=fur.assigned_to_name,
            assigned_date=fur.assigned_date,
            location=fur.location,
            condition=fur.condition,
            status=fur.status,
            remarks=fur.remarks,
            par_file_path=fur.par_file_path,
            par_number=fur.par_number,
            created_by=fur.created_by,
            created_at=fur.created_at,
            updated_at=fur.updated_at
        )
        for fur in furniture_list
    ]


@router.get("/available", response_model=List[FurnitureResponseSchema])
async def get_available_furniture(current_admin: User = Depends(get_current_admin)):
    """Get all available (unassigned) furniture - Admin only"""
    furniture_list = await Furniture.find(Furniture.status == "Available").to_list()
    
    return [
        FurnitureResponseSchema(
            id=str(fur.id),
            property_number=fur.property_number,
            gsd_code=fur.gsd_code,
            item_number=fur.item_number,
            furniture_type=fur.furniture_type,
            description=fur.description,
            brand=fur.brand,
            material=fur.material,
            color=fur.color,
            dimensions=fur.dimensions,
            acquisition_date=fur.acquisition_date,
            acquisition_cost=fur.acquisition_cost,
            assigned_to_user_id=fur.assigned_to_user_id,
            assigned_to_name=fur.assigned_to_name,
            assigned_date=fur.assigned_date,
            location=fur.location,
            condition=fur.condition,
            status=fur.status,
            remarks=fur.remarks,
            par_file_path=fur.par_file_path,
            par_number=fur.par_number,
            created_by=fur.created_by,
            created_at=fur.created_at,
            updated_at=fur.updated_at
        )
        for fur in furniture_list
    ]


@router.get("/{furniture_id}", response_model=FurnitureResponseSchema)
async def get_furniture(
    furniture_id: str,
    current_admin: User = Depends(get_current_admin)
):
    """Get single furniture by ID - Admin only"""
    furniture = await Furniture.get(furniture_id)
    
    if not furniture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Furniture not found"
        )
    
    return FurnitureResponseSchema(
        id=str(furniture.id),
        property_number=furniture.property_number,
        gsd_code=furniture.gsd_code,
        item_number=furniture.item_number,
        furniture_type=furniture.furniture_type,
        description=furniture.description,
        brand=furniture.brand,
        material=furniture.material,
        color=furniture.color,
        dimensions=furniture.dimensions,
        acquisition_date=furniture.acquisition_date,
        acquisition_cost=furniture.acquisition_cost,
        assigned_to_user_id=furniture.assigned_to_user_id,
        assigned_to_name=furniture.assigned_to_name,
        assigned_date=furniture.assigned_date,
        location=furniture.location,
        condition=furniture.condition,
        status=furniture.status,
        remarks=furniture.remarks,
        par_file_path=furniture.par_file_path,
        par_number=furniture.par_number,
        created_by=furniture.created_by,
        created_at=furniture.created_at,
        updated_at=furniture.updated_at
    )


@router.put("/{furniture_id}", response_model=FurnitureResponseSchema)
async def update_furniture(
    furniture_id: str,
    furniture_data: FurnitureUpdateSchema,
    current_admin: User = Depends(get_current_admin)
):
    """Update furniture - Admin only"""
    furniture = await Furniture.get(furniture_id)
    
    if not furniture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Furniture not found"
        )
    
    # Update fields
    update_data = furniture_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(furniture, field, value)
    
    furniture.updated_at = datetime.utcnow()
    await furniture.save()
    
    return FurnitureResponseSchema(
        id=str(furniture.id),
        property_number=furniture.property_number,
        gsd_code=furniture.gsd_code,
        item_number=furniture.item_number,
        furniture_type=furniture.furniture_type,
        description=furniture.description,
        brand=furniture.brand,
        material=furniture.material,
        color=furniture.color,
        dimensions=furniture.dimensions,
        acquisition_date=furniture.acquisition_date,
        acquisition_cost=furniture.acquisition_cost,
        assigned_to_user_id=furniture.assigned_to_user_id,
        assigned_to_name=furniture.assigned_to_name,
        assigned_date=furniture.assigned_date,
        location=furniture.location,
        condition=furniture.condition,
        status=furniture.status,
        remarks=furniture.remarks,
        par_file_path=furniture.par_file_path,
        par_number=furniture.par_number,
        created_by=furniture.created_by,
        created_at=furniture.created_at,
        updated_at=furniture.updated_at
    )


@router.delete("/{furniture_id}")
async def delete_furniture(
    furniture_id: str,
    current_admin: User = Depends(get_current_admin)
):
    """Delete furniture - Admin only"""
    furniture = await Furniture.get(furniture_id)
    
    if not furniture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Furniture not found"
        )
    
    # Check if furniture is assigned
    if furniture.status == "Assigned":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete assigned furniture. Please unassign first."
        )
    
    await furniture.delete()
    return {"message": "Furniture deleted successfully"}


@router.post("/{furniture_id}/assign", response_model=FurnitureResponseSchema)
async def assign_furniture(
    furniture_id: str,
    assign_data: FurnitureAssignSchema,
    current_admin: User = Depends(get_current_admin)
):
    """Assign furniture to user - Admin only"""
    furniture = await Furniture.get(furniture_id)
    
    if not furniture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Furniture not found"
        )
    
    # Check if already assigned
    if furniture.status == "Assigned":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Furniture is already assigned. Please unassign first or transfer."
        )
    
    # Verify user exists
    user = await User.get(assign_data.assigned_to_user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Assign furniture
    furniture.assigned_to_user_id = assign_data.assigned_to_user_id
    furniture.assigned_to_name = assign_data.assigned_to_name
    furniture.assigned_date = assign_data.assigned_date
    furniture.location = assign_data.location
    furniture.par_number = assign_data.par_number
    furniture.status = "Assigned"
    furniture.updated_at = datetime.utcnow()
    
    await furniture.save()
    
    return FurnitureResponseSchema(
        id=str(furniture.id),
        property_number=furniture.property_number,
        gsd_code=furniture.gsd_code,
        item_number=furniture.item_number,
        furniture_type=furniture.furniture_type,
        description=furniture.description,
        brand=furniture.brand,
        material=furniture.material,
        color=furniture.color,
        dimensions=furniture.dimensions,
        acquisition_date=furniture.acquisition_date,
        acquisition_cost=furniture.acquisition_cost,
        assigned_to_user_id=furniture.assigned_to_user_id,
        assigned_to_name=furniture.assigned_to_name,
        assigned_date=furniture.assigned_date,
        location=furniture.location,
        condition=furniture.condition,
        status=furniture.status,
        remarks=furniture.remarks,
        par_file_path=furniture.par_file_path,
        par_number=furniture.par_number,
        created_by=furniture.created_by,
        created_at=furniture.created_at,
        updated_at=furniture.updated_at
    )


@router.post("/{furniture_id}/unassign", response_model=FurnitureResponseSchema)
async def unassign_furniture(
    furniture_id: str,
    current_admin: User = Depends(get_current_admin)
):
    """Unassign furniture from user - Admin only"""
    furniture = await Furniture.get(furniture_id)
    
    if not furniture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Furniture not found"
        )
    
    # Unassign
    furniture.assigned_to_user_id = None
    furniture.assigned_to_name = None
    furniture.assigned_date = None
    furniture.location = None
    furniture.status = "Available"
    furniture.updated_at = datetime.utcnow()
    
    await furniture.save()
    
    return FurnitureResponseSchema(
        id=str(furniture.id),
        property_number=furniture.property_number,
        gsd_code=furniture.gsd_code,
        item_number=furniture.item_number,
        furniture_type=furniture.furniture_type,
        description=furniture.description,
        brand=furniture.brand,
        material=furniture.material,
        color=furniture.color,
        dimensions=furniture.dimensions,
        acquisition_date=furniture.acquisition_date,
        acquisition_cost=furniture.acquisition_cost,
        assigned_to_user_id=furniture.assigned_to_user_id,
        assigned_to_name=furniture.assigned_to_name,
        assigned_date=furniture.assigned_date,
        location=furniture.location,
        condition=furniture.condition,
        status=furniture.status,
        remarks=furniture.remarks,
        par_file_path=furniture.par_file_path,
        par_number=furniture.par_number,
        created_by=furniture.created_by,
        created_at=furniture.created_at,
        updated_at=furniture.updated_at
    )


# ============ USER ROUTES ============

@router.get("/my-furniture", response_model=List[FurnitureResponseSchema])
async def get_my_furniture(current_user: User = Depends(get_current_user)):
    """Get furniture assigned to current user"""
    furniture_list = await Furniture.find(
        Furniture.assigned_to_user_id == str(current_user.id)
    ).to_list()
    
    return [
        FurnitureResponseSchema(
            id=str(fur.id),
            property_number=fur.property_number,
            gsd_code=fur.gsd_code,
            item_number=fur.item_number,
            furniture_type=fur.furniture_type,
            description=fur.description,
            brand=fur.brand,
            material=fur.material,
            color=fur.color,
            dimensions=fur.dimensions,
            acquisition_date=fur.acquisition_date,
            acquisition_cost=fur.acquisition_cost,
            assigned_to_user_id=fur.assigned_to_user_id,
            assigned_to_name=fur.assigned_to_name,
            assigned_date=fur.assigned_date,
            location=fur.location,
            condition=fur.condition,
            status=fur.status,
            remarks=fur.remarks,
            par_file_path=fur.par_file_path,
            par_number=fur.par_number,
            created_by=fur.created_by,
            created_at=fur.created_at,
            updated_at=fur.updated_at
        )
        for fur in furniture_list
    ]


# ============ FILE UPLOAD (PAR DOCUMENTS) ============

@router.post("/{furniture_id}/upload-par")
async def upload_par_document(
    furniture_id: str,
    file: UploadFile = File(...),
    current_admin: User = Depends(get_current_admin)
):
    """Upload PAR document for furniture - Admin only"""
    furniture = await Furniture.get(furniture_id)
    
    if not furniture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Furniture not found"
        )
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )
    
    # Create upload directory
    upload_dir = "app/static/uploads/furniture_pars"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{furniture.property_number}_{timestamp}.pdf"
    file_path = os.path.join(upload_dir, filename)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    # Update furniture
    furniture.par_file_path = file_path
    furniture.updated_at = datetime.utcnow()
    await furniture.save()
    
    return {
        "message": "PAR document uploaded successfully",
        "file_path": file_path
    }


@router.get("/{furniture_id}/download-par")
async def download_par_document(
    furniture_id: str,
    current_user: User = Depends(get_current_user)
):
    """Download PAR document - User or Admin"""
    furniture = await Furniture.get(furniture_id)
    
    if not furniture:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Furniture not found"
        )
    
    # Check if user has access (assigned to them or admin)
    if current_user.role != "admin" and furniture.assigned_to_user_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this PAR document"
        )
    
    if not furniture.par_file_path or not os.path.exists(furniture.par_file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PAR document not found"
        )
    
    return FileResponse(
        path=furniture.par_file_path,
        filename=f"PAR_{furniture.property_number}.pdf",
        media_type="application/pdf"
    )


# ============ UTILITY ENDPOINTS ============

@router.get("/types/list")
async def get_furniture_types():
    """Get list of furniture types"""
    return {"furniture_types": FURNITURE_TYPES}