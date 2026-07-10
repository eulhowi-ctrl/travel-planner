# Travel Planner Application Package
__version__ = "1.0.0"
__author__ = "Travel Planner Team"
__description__ = "AI-Powered Travel Planning Application"

from app.database import get_db, init_db
from app.models import Base

__all__ = ["get_db", "init_db", "Base"]
