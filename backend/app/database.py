# backend/app/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import settings
from app.models.user import User
from app.models.equipment import Equipment, Furniture
from app.models.audit import AuditLog  # ✅ Add this

async def init_db():
    """Initialize database connection and collections"""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    database = client[settings.MONGODB_DB_NAME]
    
    await init_beanie(
        database=database,
        document_models=[User, Equipment, Furniture, AuditLog]  # ✅ Add AuditLog
    )
    
    # Create indexes
    await User.find_all().motor_collection.create_index("email", unique=True)
    await User.find_all().motor_collection.create_index("is_approved")
    await User.find_all().motor_collection.create_index("role")
    
    # ✅ Add audit log indexes
    await AuditLog.find_all().motor_collection.create_index("timestamp")
    await AuditLog.find_all().motor_collection.create_index("user_id")
    await AuditLog.find_all().motor_collection.create_index("resource_type")
    
    print("✅ Database initialized with indexes")