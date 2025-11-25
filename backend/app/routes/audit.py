# backend/app/routes/audit.py
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from datetime import datetime, timedelta

from app.models.user import User
from app.models.audit import AuditLog
from app.schemas.audit_schema import AuditLogResponseSchema
from app.utils.dependencies import get_current_admin

router = APIRouter(prefix="/api/audit", tags=["Audit Logs"])

@router.get("/", response_model=List[AuditLogResponseSchema])
async def get_audit_logs(
    limit: int = Query(100, ge=1, le=500),
    action: Optional[str] = None,
    resource_type: Optional[str] = None,
    user_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    current_admin: User = Depends(get_current_admin)
):
    """Get audit logs with filters - Admin only"""
    
    query = {}
    
    if action:
        query["action"] = action
    
    if resource_type:
        query["resource_type"] = resource_type
    
    if user_id:
        query["user_id"] = user_id
    
    if start_date or end_date:
        query["timestamp"] = {}
        if start_date:
            query["timestamp"]["$gte"] = start_date
        if end_date:
            query["timestamp"]["$lte"] = end_date
    
    logs = await AuditLog.find(query).sort(-AuditLog.timestamp).limit(limit).to_list()
    
    return [
        AuditLogResponseSchema(
            id=str(log.id),
            user_id=log.user_id,
            user_email=log.user_email,
            user_role=log.user_role,
            action=log.action,
            resource_type=log.resource_type,
            resource_id=log.resource_id,
            resource_name=log.resource_name,
            changes=log.changes,
            old_values=log.old_values,
            new_values=log.new_values,
            timestamp=log.timestamp
        )
        for log in logs
    ]


@router.get("/resource/{resource_type}/{resource_id}", response_model=List[AuditLogResponseSchema])
async def get_resource_history(
    resource_type: str,
    resource_id: str,
    current_admin: User = Depends(get_current_admin)
):
    """Get complete history of a specific resource - Admin only"""
    
    logs = await AuditLog.find(
        AuditLog.resource_type == resource_type.upper(),
        AuditLog.resource_id == resource_id
    ).sort(-AuditLog.timestamp).to_list()
    
    return [
        AuditLogResponseSchema(
            id=str(log.id),
            user_id=log.user_id,
            user_email=log.user_email,
            user_role=log.user_role,
            action=log.action,
            resource_type=log.resource_type,
            resource_id=log.resource_id,
            resource_name=log.resource_name,
            changes=log.changes,
            old_values=log.old_values,
            new_values=log.new_values,
            timestamp=log.timestamp
        )
        for log in logs
    ]


@router.get("/stats")
async def get_audit_stats(
    days: int = Query(30, ge=1, le=365),
    current_admin: User = Depends(get_current_admin)
):
    """Get audit statistics - Admin only"""
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    logs = await AuditLog.find(
        AuditLog.timestamp >= start_date
    ).to_list()
    
    # Calculate stats
    actions_count = {}
    resource_types_count = {}
    users_count = {}
    
    for log in logs:
        actions_count[log.action] = actions_count.get(log.action, 0) + 1
        resource_types_count[log.resource_type] = resource_types_count.get(log.resource_type, 0) + 1
        users_count[log.user_email] = users_count.get(log.user_email, 0) + 1
    
    return {
        "total_actions": len(logs),
        "date_range": {
            "start": start_date,
            "end": datetime.utcnow(),
            "days": days
        },
        "actions_breakdown": actions_count,
        "resource_types_breakdown": resource_types_count,
        "most_active_users": dict(sorted(users_count.items(), key=lambda x: x[1], reverse=True)[:10])
    }