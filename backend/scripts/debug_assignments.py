# backend/scripts/debug_assignments.py
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config import settings
from app.models.user import User
from app.models.equipment import Equipment

async def debug_assignments():
    """Debug script to check equipment assignments"""
    print("🔍 Debugging Equipment Assignments...\n")
    
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    database = client[settings.MONGODB_DB_NAME]
    
    await init_beanie(
        database=database,
        document_models=[User, Equipment]
    )
    
    # Get all users
    print("=" * 60)
    print("USERS IN DATABASE")
    print("=" * 60)
    users = await User.find_all().to_list()
    for user in users:
        print(f"ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Name: {user.full_name}")
        print(f"Role: {user.role}")
        print(f"Approved: {user.is_approved}")
        print("-" * 60)
    
    # Get all equipment
    print("\n" + "=" * 60)
    print("EQUIPMENT IN DATABASE")
    print("=" * 60)
    all_equipment = await Equipment.find_all().to_list()
    print(f"Total Equipment: {len(all_equipment)}\n")
    
    for eq in all_equipment:
        print(f"Property Number: {eq.property_number}")
        print(f"Brand/Model: {eq.brand} {eq.model}")
        print(f"Status: {eq.status}")
        print(f"Assigned To User ID: '{eq.assigned_to_user_id}'")
        print(f"Assigned To Name: {eq.assigned_to_name}")
        
        # Check if this ID matches any user
        if eq.assigned_to_user_id:
            matching_user = None
            for user in users:
                if str(user.id) == eq.assigned_to_user_id:
                    matching_user = user
                    break
            
            if matching_user:
                print(f"✅ MATCH FOUND: {matching_user.email}")
            else:
                print(f"❌ NO MATCH: User ID '{eq.assigned_to_user_id}' not found")
                print(f"   Available User IDs:")
                for user in users:
                    print(f"   - {user.id} ({user.email})")
        
        print("-" * 60)
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    assigned_count = len([eq for eq in all_equipment if eq.assigned_to_user_id])
    print(f"Total Equipment: {len(all_equipment)}")
    print(f"Assigned Equipment: {assigned_count}")
    print(f"Available Equipment: {len(all_equipment) - assigned_count}")
    
    client.close()
    print("\n✅ Debug complete!")

if __name__ == "__main__":
    asyncio.run(debug_assignments())