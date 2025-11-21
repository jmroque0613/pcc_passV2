from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.config import settings
from app.models.user import User

async def init_db():
    """Initialize database connection and collections"""
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    database = client[settings.MONGODB_DB_NAME]
    
    await init_beanie(
        database=database,
        document_models=[User]
    )
    
    # Create indexes
    await User.find_all().motor_collection.create_index("email", unique=True)
    await User.find_all().motor_collection.create_index("is_approved")
    await User.find_all().motor_collection.create_index("role")
    
    print("✅ Database initialized with indexes")
