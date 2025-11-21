import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings
from app.models.user import User

async def init_database():
    """Initialize MongoDB database and create indexes"""
    print("🔄 Initializing PCC-PASS Database...")
    
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    database = client[settings.MONGODB_DB_NAME]
    
    # Initialize beanie
    await init_beanie(
        database=database,
        document_models=[User]
    )
    
    # Create indexes
    print("📑 Creating indexes...")
    
    await User.find_all().motor_collection.create_index("email", unique=True)
    await User.find_all().motor_collection.create_index("is_approved")
    await User.find_all().motor_collection.create_index("role")
    
    print("✅ Database initialized successfully!")
    print(f"📦 Database Name: {settings.MONGODB_DB_NAME}")
    print(f"🔗 MongoDB URL: {settings.MONGODB_URL}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(init_database())