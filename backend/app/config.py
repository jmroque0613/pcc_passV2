from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # MongoDB
    MONGODB_URL: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "pcc_pass_db2"
    
    # JWT
    SECRET_KEY: str = "PCC-SECRET-KET"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Admin
    ADMIN_SECRET_KEY: str = "PCC-ADMIN-2025"
    
    # CORS
    FRONTEND_URL: str = "http://localhost:4200"
    
    class Config:
        env_file = ".env"

# Create settings instance - THIS IS IMPORTANT!
settings = Settings()