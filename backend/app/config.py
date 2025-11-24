# backend/app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "pcc_pass_db2"
    
    # JWT
    SECRET_KEY: str = "PCC-2025"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # Admin
    ADMIN_SECRET_KEY: str = "PCC-ADMIN-2025"
    
    # CORS - UPDATED for network access
    FRONTEND_URL: str = "http://172.16.2.4:4200"
    
    class Config:
        env_file = ".env"

# Create settings instance
settings = Settings()