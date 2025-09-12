import os
import logging
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

logger = logging.getLogger(__name__)

# Database configuration
DATABASE_URL = "sqlite:///./data/vkr_exports.db"

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=False  # Set to True for SQL query logging
)

def create_db_and_tables():
    """Create database tables"""
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Create all tables
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise

def get_session() -> Generator[Session, None, None]:
    """Get database session"""
    with Session(engine) as session:
        yield session

def init_db():
    """Initialize database"""
    create_db_and_tables()
    logger.info("Database initialized successfully")




