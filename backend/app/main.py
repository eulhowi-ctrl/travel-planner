from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path

# Import models to create tables
from app.models import Base
from app.database import engine, init_db, SessionLocal

# Create tables on startup
Base.metadata.create_all(bind=engine)

# Load sample data on startup (in-memory database, so data persists during app lifecycle)
try:
    from app.utils.seed_data import seed_destinations, seed_long_distance_transportation, seed_local_transportation
    db = SessionLocal()
    seed_destinations(db)
    seed_long_distance_transportation(db)
    seed_local_transportation(db)
    db.close()
    print("✅ Sample data loaded successfully")
except Exception as e:
    print(f"⚠️  Sample data loading skipped: {e}")

# Initialize FastAPI app
app = FastAPI(
    title="Travel Planner API",
    description="API for AI-powered travel planning application",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# CORS middleware configuration
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create static directories
static_dir = Path("static")
qr_dir = static_dir / "qr_codes"
qr_dir.mkdir(parents=True, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# ==================== Health Check ====================


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": __import__("datetime").datetime.utcnow().isoformat()
    }


@app.get("/api/v1/health")
async def api_health_check():
    """API health check endpoint"""
    return {
        "status": "healthy",
        "api": "Travel Planner API",
        "version": "1.0.0",
        "timestamp": __import__("datetime").datetime.utcnow().isoformat()
    }


# ==================== API Routers ====================
from app.routers import users, destinations, itineraries, budgets, transportation, qrcodes

# Include routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(destinations.router, prefix="/api/v1/destinations", tags=["destinations"])
app.include_router(itineraries.router, prefix="/api/v1/itineraries", tags=["itineraries"])
app.include_router(budgets.router, prefix="/api/v1/budgets", tags=["budgets"])
app.include_router(transportation.router, prefix="/api/v1/transportation", tags=["transportation"])
app.include_router(qrcodes.router, prefix="/api/v1/qr-codes", tags=["qr-codes"])

# Mount frontend at root (SPA fallback to index.html)
frontend_dir = Path(__file__).parent.parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn

    # Get configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    debug = os.getenv("DEBUG", "False") == "True"

    # Run server
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )
