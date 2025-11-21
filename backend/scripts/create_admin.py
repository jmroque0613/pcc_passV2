import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings
from app.models.user import User
from app.utils.security import hash_password

async def create_admin():
    """Create an initial admin user"""
    print("🔄 Creating Admin User...")
    
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    database = client[settings.MONGODB_DB_NAME]
    
    await init_beanie(
        database=database,
        document_models=[User]
    )
    
    # Admin details
    admin_email = input("Enter admin email: ")
    admin_password = input("Enter admin password: ")
    
    # Check if admin already exists
    existing_admin = await User.find_one(User.email == admin_email)
    if existing_admin:
        print("❌ Admin with this email already exists!")
        client.close()
        return
    
    # Create admin user
    admin = User(
        surname="Admin",
        first_name="System",
        middle_name=None,
        email=admin_email,
        password_hash=hash_password(admin_password),
        position="System Administrator",
        salary_grade="SG 30",
        starting_date=datetime.utcnow(),
        job_category="Regular Employee",
        assigned_unit="Office of the Exec. Director",
        role="admin",
        is_approved=True,
        is_active=True
    )
    
    await admin.insert()
    
    print("✅ Admin user created successfully!")
    print(f"📧 Email: {admin_email}")
    print(f"🔑 Role: {admin.role}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(create_admin())