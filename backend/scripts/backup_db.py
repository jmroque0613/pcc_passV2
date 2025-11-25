# scripts/backup_db.py
import asyncio
from datetime import datetime
import subprocess

async def backup_database():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_{timestamp}.gz"
    
    subprocess.run([
        "mongodump",
        "--uri", settings.MONGODB_URL,
        "--db", settings.MONGODB_DB_NAME,
        "--archive", backup_file,
        "--gzip"
    ])