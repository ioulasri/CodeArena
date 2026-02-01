from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_router
from app.core.database import engine, Base
import os

# Create database tables
Base.metadata.create_all(bind=engine)

# Configure CORS from environment for easier local testing on different devices
cors_allow_all = os.getenv('CORS_ALLOW_ALL', 'false').lower() in ('1', 'true', 'yes')
cors_origins_env = os.getenv('CORS_ALLOW_ORIGINS')
if cors_allow_all:
    allowed_origins = ["*"]
elif cors_origins_env:
    # comma-separated origins
    allowed_origins = [o.strip() for o in cors_origins_env.split(',') if o.strip()]
else:
    # Allow common development origins
    # This allows localhost/127.0.0.1 frontends to access the backend on any local IP
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "http://192.168.100.2:3000",
        "http://192.168.100.2:8000",
    ]

app = FastAPI(
    title="CodeArena API",
    description="Competitive programming platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware - must be added before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "message": "Welcome to CodeArena API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}
