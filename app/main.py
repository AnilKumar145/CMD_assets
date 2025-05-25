from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.logging_config import setup_logging
from app.middleware.monitoring import MonitoringMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.routers import AssetsRouter
from app.database import engine, Base

# Setup logging
logger = setup_logging("assets-service")

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Assets Microservice",
    description="API for managing assets",
    version="1.0.0",
    # Use standard paths for docs or specify custom paths
    docs_url="/docs",  # Changed from /api/assets/docs
    redoc_url="/redoc",  # Changed from /api/assets/redoc
    openapi_url="/openapi.json"  # Changed from /api/assets/openapi.json
)

# Add middlewares
app.add_middleware(MonitoringMiddleware)
app.add_middleware(RateLimitMiddleware, requests_per_minute=100)  # Adjust the limit as needed

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers - Note: Don't include the prefix here since it's already in the router
app.include_router(AssetsRouter.router)

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "assets-service"}
