# backend/app/services/audit_service.py
from typing import Dict, Optional
from datetime import datetime
from app.models.audit import AuditLog
from app.models.user import User

class AuditService:
    """Service for creating audit logs"""
    
    @staticmethod
    async def log_action(
        user: User,
        action: str,
        resource_type: str,
        resource_id: str,
        resource_name: Optional[str] = None,
        changes: Optional[Dict] = None,
        old_values: Optional[Dict] = None,
        new_values: Optional[Dict] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        notes: Optional[str] = None
    ):
        """
        Create an audit log entry
        
        Args:
            user: User who performed the action
            action: Action performed (CREATE, UPDATE, DELETE, ASSIGN, etc.)
            resource_type: Type of resource (EQUIPMENT, FURNITURE, USER)
            resource_id: ID of the affected resource
            resource_name: Name/description of the resource
            changes: Summary of changes
            old_values: Previous values
            new_values: New values
            ip_address: IP address of the user
            user_agent: Browser/client info
            notes: Additional notes
        """
        audit_log = AuditLog(
            user_id=str(user.id),
            user_email=user.email,
            user_role=user.role,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            resource_name=resource_name,
            changes=changes or {},
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
            notes=notes
        )
        
        await audit_log.insert()
        print(f"📝 Audit Log: {user.email} - {action} - {resource_type} - {resource_id}")
        return audit_log
    
    @staticmethod
    async def get_user_activity(user_id: str, limit: int = 50):
        """Get recent activity for a specific user"""
        return await AuditLog.find(
            AuditLog.user_id == user_id
        ).sort(-AuditLog.timestamp).limit(limit).to_list()
    
    @staticmethod
    async def get_resource_history(resource_type: str, resource_id: str):
        """Get complete history of a specific resource"""
        return await AuditLog.find(
            AuditLog.resource_type == resource_type,
            AuditLog.resource_id == resource_id
        ).sort(-AuditLog.timestamp).to_list()
    
    @staticmethod
    async def get_recent_activity(limit: int = 100):
        """Get recent system-wide activity"""
        return await AuditLog.find_all().sort(-AuditLog.timestamp).limit(limit).to_list()