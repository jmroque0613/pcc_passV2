# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from contextlib import asynccontextmanager
import os

from app.config import settings
from app.models.user import User
from app.models.equipment import Equipment, Furniture
from app.routes import auth, admin, equipment, furniture

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to MongoDB
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    database = client[settings.MONGODB_DB_NAME]
    
    # Initialize beanie with ALL document models
    await init_beanie(
        database=database,
        document_models=[User, Equipment, Furniture]
    )
    
    print("✅ Connected to MongoDB")
    print(f"📦 Database: {settings.MONGODB_DB_NAME}")
    print("📋 Collections initialized: users, equipment, furniture")
    
    # Create upload directories
    os.makedirs("app/static/uploads/equipment_pars", exist_ok=True)
    os.makedirs("app/static/uploads/furniture_pars", exist_ok=True)
    os.makedirs("app/static/uploads/hr_files", exist_ok=True)
    print("📁 Upload directories created")
    
    yield
    
    # Shutdown: Close MongoDB connection
    client.close()
    print("❌ Disconnected from MongoDB")

# Create FastAPI app
app = FastAPI(
    title="PCC-PASS API",
    description="Phil Cancer Center Personnel and Supplies System",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration - UPDATED for network access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "http://172.16.2.4:4200",  # Your IP
        "http://172.16.2.4:8000",  # Backend IP
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploads
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(equipment.router)
app.include_router(furniture.router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to PCC-PASS API",
        "version": "1.0.0",
        "docs": "/docs",
        "modules": ["Authentication", "Admin", "Equipment", "Furniture"]
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "collections": ["users", "equipment", "furniture"]
    }