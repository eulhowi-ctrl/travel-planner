from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL from environment
# Use in-memory SQLite for production (faster performance)
# Data is not persisted across restarts, but provides optimal performance for Render
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

# Create database engine
if DATABASE_URL.startswith("sqlite"):
    # SQLite doesn't support NullPool
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=os.getenv("DEBUG", "False") == "True"
    )
else:
    # PostgreSQL with NullPool for connection management
    engine = create_engine(
        DATABASE_URL,
        poolclass=NullPool,
        echo=os.getenv("DEBUG", "False") == "True"
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    from app.models import Base
    Base.metadata.create_all(bind=engine)
