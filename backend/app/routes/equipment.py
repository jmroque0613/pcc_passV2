# backend/app/routes/equipment.py
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from fastapi.responses import FileResponse
import aiofiles
import os

from app.models.user import User
from app.models.equipment import Equipment, EQUIPMENT_TYPES, CONDITIONS, STATUSES
from app.schemas.equipment_schema import (
    EquipmentCreateSchema,
    EquipmentUpdateSchema,
    EquipmentAssignSchema,
    EquipmentResponseSchema,
    EquipmentTransferSchema
)
from app.utils.dependencies import get_current_admin, get_current_user
from app.services.audit_service import AuditService

router = APIRouter(prefix="/api/equipment", tags=["Equipment"])


# Add this debugging endpoint temporarily to check what's happening
@router.get("/debug/my-info")
async def debug_my_info(current_user: User = Depends(get_current_user)):
    """Debug endpoint to check user info"""
    return {
        "user_id": str(current_user.id),
        "user_email": current_user.email,
        "user_role": current_user.role,
        "user_approved": current_user.is_approved
    }

# ============ USER ROUTES - MUST BE BEFORE /{equipment_id} ROUTE ============
@router.get("/my-equipment", response_model=List[EquipmentResponseSchema])
async def get_my_equipment(current_user: User = Depends(get_current_user)):
    """Get equipment assigned to current user - USER ACCESS"""
    
    # Debug logging
    user_id_str = str(current_user.id)
    print(f"🔍 DEBUG - User requesting equipment:")
    print(f"   Email: {current_user.email}")
    print(f"   User ID: {user_id_str}")
    print(f"   Role: {current_user.role}")
    print(f"   Approved: {current_user.is_approved}")
    
    # Try to find ALL equipment first to debug
    all_equipment = await Equipment.find_all().to_list()
    print(f"📊 Total equipment in database: {len(all_equipment)}")
    
    # Show assigned equipment IDs
    assigned_equipment = [eq for eq in all_equipment if eq.assigned_to_user_id]
    print(f"📊 Total assigned equipment: {len(assigned_equipment)}")
    for eq in assigned_equipment:
        print(f"   - {eq.brand} {eq.model}: assigned_to_user_id = '{eq.assigned_to_user_id}'")
    
    # Now try the actual query
    equipment_list = await Equipment.find(
        Equipment.assigned_to_user_id == user_id_str
    ).to_list()
    
    print(f"✅ Found {len(equipment_list)} equipment items for user {user_id_str}")
    
    if len(equipment_list) == 0:
        print("⚠️  No equipment found. Checking if there's a mismatch...")
        # Check if any equipment has similar ID
        for eq in all_equipment:
            if eq.assigned_to_user_id and user_id_str in str(eq.assigned_to_user_id):
                print(f"⚠️  Found similar: {eq.assigned_to_user_id} vs {user_id_str}")
    
    return [
        EquipmentResponseSchema(
            id=str(eq.id),
            property_number=eq.property_number,
            gsd_code=eq.gsd_code,
            item_number=eq.item_number,
            equipment_type=eq.equipment_type,
            brand=eq.brand,
            model=eq.model,
            serial_number=eq.serial_number,
            specifications=eq.specifications,
            acquisition_date=eq.acquisition_date,
            acquisition_cost=eq.acquisition_cost,
            assigned_to_user_id=eq.assigned_to_user_id,
            assigned_to_name=eq.assigned_to_name,
            assigned_date=eq.assigned_date,
            assignment_type=eq.assignment_type,
            previous_recipient=eq.previous_recipient,
            condition=eq.condition,
            status=eq.status,
            remarks=eq.remarks,
            par_file_path=eq.par_file_path,
            par_number=eq.par_number,
            created_by=eq.created_by,
            created_at=eq.created_at,
            updated_at=eq.updated_at
        )
        for eq in equipment_list
    ]

# ============ UTILITY ENDPOINTS - BEFORE PARAMETERIZED ROUTES ============
@router.get("/assignment-types/list")
async def get_assignment_types():
    """Get list of assignment types"""
    from app.models.equipment import ASSIGNMENT_TYPES
    return {"assignment_types": ASSIGNMENT_TYPES}


@router.get("/types/list")
async def get_equipment_types():
    """Get list of equipment types"""
    return {"equipment_types": EQUIPMENT_TYPES}

@router.get("/stats")
async def get_equipment_stats(current_admin: User = Depends(get_current_admin)):
    return {
        "total": await Equipment.count(),
        "available": await Equipment.find(Equipment.status == "Available").count(),
        "assigned": await Equipment.find(Equipment.status == "Assigned").count(),
        "under_repair": await Equipment.find(Equipment.status == "Under Repair").count()
    }

@router.get("/conditions/list")
async def get_conditions():
    """Get list of equipment conditions"""
    return {"conditions": CONDITIONS}


@router.get("/statuses/list")
async def get_statuses():
    """Get list of equipment statuses"""
    return {"statuses": STATUSES}


@router.get("/available", response_model=List[EquipmentResponseSchema])
async def get_available_equipment(current_admin: User = Depends(get_current_admin)):
    """Get all available (unassigned) equipment - Admin only"""
    equipment_list = await Equipment.find(Equipment.status == "Available").to_list()
    
    return [
        EquipmentResponseSchema(
            id=str(eq.id),
            property_number=eq.property_number,
            gsd_code=eq.gsd_code,
            item_number=eq.item_number,
            equipment_type=eq.equipment_type,
            brand=eq.brand,
            model=eq.model,
            serial_number=eq.serial_number,
            specifications=eq.specifications,
            acquisition_date=eq.acquisition_date,
            acquisition_cost=eq.acquisition_cost,
            assigned_to_user_id=eq.assigned_to_user_id,
            assigned_to_name=eq.assigned_to_name,
            assigned_date=eq.assigned_date,
            previous_recipient=eq.previous_recipient,
            condition=eq.condition,
            status=eq.status,
            remarks=eq.remarks,
            par_file_path=eq.par_file_path,
            par_number=eq.par_number,
            created_by=eq.created_by,
            created_at=eq.created_at,
            updated_at=eq.updated_at
        )
        for eq in equipment_list
    ]


# ============ ADMIN ROUTES ============

@router.post("/", response_model=EquipmentResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_equipment(
    equipment_data: EquipmentCreateSchema,
    current_admin: User = Depends(get_current_admin)
):
    """Create new equipment - Admin only"""
    
    # Check if property number already exists
    existing = await Equipment.find_one(Equipment.property_number == equipment_data.property_number)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Property number already exists"
        )
    
    # Create equipment
    new_equipment = Equipment(
        property_number=equipment_data.property_number,
        gsd_code=equipment_data.gsd_code,
        item_number=equipment_data.item_number,
        equipment_type=equipment_data.equipment_type,
        brand=equipment_data.brand,
        model=equipment_data.model,
        serial_number=equipment_data.serial_number,
        specifications=equipment_data.specifications,
        acquisition_date=equipment_data.acquisition_date,
        acquisition_cost=equipment_data.acquisition_cost,
        condition=equipment_data.condition,
        status=equipment_data.status,
        remarks=equipment_data.remarks,
        created_by=current_admin.email
    )
    
    await new_equipment.insert()

    await AuditService.log_action(
    user=current_admin,
    action="CREATE",
    resource_type="EQUIPMENT",
    resource_id=str(new_equipment.id),
    resource_name=f"{new_equipment.brand} {new_equipment.model}",
    changes={
        "property_number": new_equipment.property_number,
        "equipment_type": new_equipment.equipment_type,
        "status": new_equipment.status
    },
    new_values={
        "property_number": new_equipment.property_number,
        "equipment_type": new_equipment.equipment_type,
        "brand": new_equipment.brand,
        "model": new_equipment.model,
        "status": new_equipment.status
    }
)
    
    return EquipmentResponseSchema(
        id=str(new_equipment.id),
        property_number=new_equipment.property_number,
        gsd_code=new_equipment.gsd_code,
        item_number=new_equipment.item_number,
        equipment_type=new_equipment.equipment_type,
        brand=new_equipment.brand,
        model=new_equipment.model,
        serial_number=new_equipment.serial_number,
        specifications=new_equipment.specifications,
        acquisition_date=new_equipment.acquisition_date,
        acquisition_cost=new_equipment.acquisition_cost,
        assigned_to_user_id=new_equipment.assigned_to_user_id,
        assigned_to_name=new_equipment.assigned_to_name,
        assigned_date=new_equipment.assigned_date,
        previous_recipient=new_equipment.previous_recipient,
        condition=new_equipment.condition,
        status=new_equipment.status,
        remarks=new_equipment.remarks,
        par_file_path=new_equipment.par_file_path,
        par_number=new_equipment.par_number,
        created_by=new_equipment.created_by,
        created_at=new_equipment.created_at,
        updated_at=new_equipment.updated_at
    )


@router.get("/", response_model=List[EquipmentResponseSchema])
async def get_all_equipment(
    skip: int = 0,
    limit: int = 100,
    current_admin: User = Depends(get_current_admin)
):
    """Get all equipment with pagination - Admin only"""

    # Fetch with pagination
    equipment_list = (
        await Equipment.find_all()
        .skip(skip)
        .limit(limit)
        .to_list()
    )

    # Convert to response model
    return [
        EquipmentResponseSchema(
            id=str(eq.id),
            **eq.model_dump(exclude={"id"})   # Pydantic v2
        )
        for eq in equipment_list
    ]



@router.get("/search")
async def search_equipment(
    query: str,
    equipment_type: Optional[str] = None,
    status: Optional[str] = None,
    current_admin: User = Depends(get_current_admin)
):
    filters = {}
    if equipment_type:
        filters["equipment_type"] = equipment_type
    if status:
        filters["status"] = status
    # Add text search logic


@router.get("/{equipment_id}", response_model=EquipmentResponseSchema)
async def get_equipment(
    equipment_id: str,
    current_admin: User = Depends(get_current_admin)
):
    """Get single equipment by ID - Admin only"""
    equipment = await Equipment.get(equipment_id)
    
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipment not found"
        )
    
    return EquipmentResponseSchema(
        id=str(equipment.id),
        property_number=equipment.property_number,
        gsd_code=equipment.gsd_code,
        item_number=equipment.item_number,
        equipment_type=equipment.equipment_type,
        brand=equipment.brand,
        model=equipment.model,
        serial_number=equipment.serial_number,
        specifications=equipment.specifications,
        acquisition_date=equipment.acquisition_date,
        acquisition_cost=equipment.acquisition_cost,
        assigned_to_user_id=equipment.assigned_to_user_id,
        assigned_to_name=equipment.assigned_to_name,
        assigned_date=equipment.assigned_date,
        previous_recipient=equipment.previous_recipient,
        condition=equipment.condition,
        status=equipment.status,
        remarks=equipment.remarks,
        par_file_path=equipment.par_file_path,
        par_number=equipment.par_number,
        created_by=equipment.created_by,
        created_at=equipment.created_at,
        updated_at=equipment.updated_at
    )

@router.post("/{equipment_id}/transfer")
async def transfer_equipment(
    equipment_id: str,
    transfer_data: EquipmentTransferSchema,
    current_admin: User = Depends(get_current_admin)
):
    # Transfer from one user to another with history tracking
    pass


@router.put("/{equipment_id}", response_model=EquipmentResponseSchema)
async def update_equipment(
    equipment_id: str,
    equipment_data: EquipmentUpdateSchema,
    current_admin: User = Depends(get_current_admin)
):
    """Update equipment - Admin only"""
    equipment = await Equipment.get(equipment_id)
    
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipment not found"
        )
    
        # ✅ CAPTURE OLD VALUES
    old_values = {
        "property_number": equipment.property_number,
        "equipment_type": equipment.equipment_type,
        "brand": equipment.brand,
        "model": equipment.model,
        "status": equipment.status,
        "condition": equipment.condition
    }

    # Update fields
    update_data = equipment_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(equipment, field, value)
    
    equipment.updated_at = datetime.utcnow()
    await equipment.save()

        # ✅ CAPTURE NEW VALUES
    new_values = {
        "property_number": equipment.property_number,
        "equipment_type": equipment.equipment_type,
        "brand": equipment.brand,
        "model": equipment.model,
        "status": equipment.status,
        "condition": equipment.condition
    }

        # ✅ ADD AUDIT LOG
    await AuditService.log_action(
        user=current_admin,
        action="UPDATE",
        resource_type="EQUIPMENT",
        resource_id=str(equipment.id),
        resource_name=f"{equipment.brand} {equipment.model}",
        changes=update_data,
        old_values=old_values,
        new_values=new_values
    )
    
    return EquipmentResponseSchema(
        id=str(equipment.id),
        property_number=equipment.property_number,
        gsd_code=equipment.gsd_code,
        item_number=equipment.item_number,
        equipment_type=equipment.equipment_type,
        brand=equipment.brand,
        model=equipment.model,
        serial_number=equipment.serial_number,
        specifications=equipment.specifications,
        acquisition_date=equipment.acquisition_date,
        acquisition_cost=equipment.acquisition_cost,
        assigned_to_user_id=equipment.assigned_to_user_id,
        assigned_to_name=equipment.assigned_to_name,
        assigned_date=equipment.assigned_date,
        previous_recipient=equipment.previous_recipient,
        condition=equipment.condition,
        status=equipment.status,
        remarks=equipment.remarks,
        par_file_path=equipment.par_file_path,
        par_number=equipment.par_number,
        created_by=equipment.created_by,
        created_at=equipment.created_at,
        updated_at=equipment.updated_at
    )


@router.delete("/{equipment_id}")
async def delete_equipment(
    equipment_id: str,
    current_admin: User = Depends(get_current_admin)
):
    """Delete equipment - Admin only"""
    equipment = await Equipment.get(equipment_id)
    
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipment not found"
        )
    
    # Check if equipment is assigned
    if equipment.status == "Assigned":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete assigned equipment. Please unassign first."
        )
    
    # ✅ CAPTURE INFO BEFORE DELETE
    equipment_info = f"{equipment.brand} {equipment.model} ({equipment.property_number})"
    
    await equipment.delete()
    # ✅ ADD AUDIT LOG
    await AuditService.log_action(
        user=current_admin,
        action="DELETE",
        resource_type="EQUIPMENT",
        resource_id=equipment_id,
        resource_name=equipment_info,
        old_values={
            "property_number": equipment.property_number,
            "equipment_type": equipment.equipment_type,
            "brand": equipment.brand,
            "model": equipment.model,
            "status": equipment.status
        }
    )
    
    return {"message": "Equipment deleted successfully"}


@router.post("/{equipment_id}/assign", response_model=EquipmentResponseSchema)
async def assign_equipment(
    equipment_id: str,
    assign_data: EquipmentAssignSchema,
    current_admin: User = Depends(get_current_admin)
):
    """Assign equipment to user - Admin only"""
    equipment = await Equipment.get(equipment_id)
    
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipment not found"
        )
    
    # Check if already assigned
    if equipment.status == "Assigned":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Equipment is already assigned. Please unassign first or transfer."
        )
    
    # Validate assignment type
    if assign_data.assignment_type not in ["PAR", "Job Order"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assignment type must be either 'PAR' or 'Job Order'"
        )
    
    # Validate PAR number for PAR assignments
    if assign_data.assignment_type == "PAR" and not assign_data.par_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="PAR number is required for PAR assignments"
        )
    
    # Verify user exists
    user = await User.get(assign_data.assigned_to_user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Assign equipment
    equipment.assigned_to_user_id = assign_data.assigned_to_user_id
    equipment.assigned_to_name = assign_data.assigned_to_name
    equipment.assigned_date = assign_data.assigned_date
    equipment.assignment_type = assign_data.assignment_type  # NEW
    equipment.previous_recipient = assign_data.previous_recipient
    equipment.par_number = assign_data.par_number if assign_data.assignment_type == "PAR" else None
    equipment.status = "Assigned"
    equipment.updated_at = datetime.utcnow()
    
    # ✅ CAPTURE OLD STATE
    old_status = equipment.status
    old_assigned = equipment.assigned_to_name
    
    # Assign equipment
    equipment.assigned_to_user_id = assign_data.assigned_to_user_id
    equipment.assigned_to_name = assign_data.assigned_to_name
    equipment.assigned_date = assign_data.assigned_date
    equipment.assignment_type = assign_data.assignment_type
    equipment.previous_recipient = assign_data.previous_recipient
    equipment.par_number = assign_data.par_number if assign_data.assignment_type == "PAR" else None
    equipment.status = "Assigned"
    equipment.updated_at = datetime.utcnow()
    
    await equipment.save()
    
    # ✅ ADD AUDIT LOG
    await AuditService.log_action(
        user=current_admin,
        action="ASSIGN",
        resource_type="EQUIPMENT",
        resource_id=str(equipment.id),
        resource_name=f"{equipment.brand} {equipment.model}",
        changes={
            "assigned_to": assign_data.assigned_to_name,
            "assignment_type": assign_data.assignment_type,
            "status": "Assigned"
        },
        old_values={
            "status": old_status,
            "assigned_to": old_assigned
        },
        new_values={
            "status": "Assigned",
            "assigned_to": assign_data.assigned_to_name,
            "assignment_type": assign_data.assignment_type
        }
    )
    
    return EquipmentResponseSchema(
        id=str(equipment.id),
        property_number=equipment.property_number,
        gsd_code=equipment.gsd_code,
        item_number=equipment.item_number,
        equipment_type=equipment.equipment_type,
        brand=equipment.brand,
        model=equipment.model,
        serial_number=equipment.serial_number,
        specifications=equipment.specifications,
        acquisition_date=equipment.acquisition_date,
        acquisition_cost=equipment.acquisition_cost,
        assigned_to_user_id=equipment.assigned_to_user_id,
        assigned_to_name=equipment.assigned_to_name,
        assigned_date=equipment.assigned_date,
        assignment_type=equipment.assignment_type,  # NEW
        previous_recipient=equipment.previous_recipient,
        condition=equipment.condition,
        status=equipment.status,
        remarks=equipment.remarks,
        par_file_path=equipment.par_file_path,
        par_number=equipment.par_number,
        created_by=equipment.created_by,
        created_at=equipment.created_at,
        updated_at=equipment.updated_at
    )

@router.post("/{equipment_id}/unassign", response_model=EquipmentResponseSchema)
async def unassign_equipment(
    equipment_id: str,
    current_admin: User = Depends(get_current_admin)
):
    """Unassign equipment from user - Admin only"""
    equipment = await Equipment.get(equipment_id)
    
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipment not found"
        )
    
    # Store previous recipient
    if equipment.assigned_to_name:
        equipment.previous_recipient = equipment.assigned_to_name
    
    # Unassign
    equipment.assigned_to_user_id = None
    equipment.assigned_to_name = None
    equipment.assigned_date = None
    equipment.status = "Available"
    equipment.updated_at = datetime.utcnow()
    
    await equipment.save()
    
    return EquipmentResponseSchema(
        id=str(equipment.id),
        property_number=equipment.property_number,
        gsd_code=equipment.gsd_code,
        item_number=equipment.item_number,
        equipment_type=equipment.equipment_type,
        brand=equipment.brand,
        model=equipment.model,
        serial_number=equipment.serial_number,
        specifications=equipment.specifications,
        acquisition_date=equipment.acquisition_date,
        acquisition_cost=equipment.acquisition_cost,
        assigned_to_user_id=equipment.assigned_to_user_id,
        assigned_to_name=equipment.assigned_to_name,
        assigned_date=equipment.assigned_date,
        previous_recipient=equipment.previous_recipient,
        condition=equipment.condition,
        status=equipment.status,
        remarks=equipment.remarks,
        par_file_path=equipment.par_file_path,
        par_number=equipment.par_number,
        created_by=equipment.created_by,
        created_at=equipment.created_at,
        updated_at=equipment.updated_at
    )


# ============ FILE UPLOAD (PAR DOCUMENTS) ============

@router.post("/{equipment_id}/upload-par")
async def upload_par_document(
    equipment_id: str,
    file: UploadFile = File(...),
    current_admin: User = Depends(get_current_admin)
):
    
        # Add file size limit (e.g., 10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File too large. Maximum size is 10MB"
        )
    
    """Upload PAR document for equipment - Admin only"""
    equipment = await Equipment.get(equipment_id)
    
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipment not found"
        )
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed"
        )
    
    # Create upload directory
    upload_dir = "app/static/uploads/equipment_pars"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{equipment.property_number}_{timestamp}.pdf"
    file_path = os.path.join(upload_dir, filename)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    # Update equipment
    equipment.par_file_path = file_path
    equipment.updated_at = datetime.utcnow()
    await equipment.save()
    
    return {
        "message": "PAR document uploaded successfully",
        "file_path": file_path
    }


@router.get("/{equipment_id}/download-par")
async def download_par_document(
    equipment_id: str,
    current_user: User = Depends(get_current_user)
):
    """Download PAR document - User or Admin"""
    equipment = await Equipment.get(equipment_id)
    
    if not equipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Equipment not found"
        )
    
    # Check if user has access (assigned to them or admin)
    if current_user.role != "admin" and equipment.assigned_to_user_id != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this PAR document"
        )
    
    if not equipment.par_file_path or not os.path.exists(equipment.par_file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PAR document not found"
        )
    
    return FileResponse(
        path=equipment.par_file_path,
        filename=f"PAR_{equipment.property_number}.pdf",
        media_type="application/pdf"
    )