import database
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)

# database.py
try:
    engine = database.get_connection()  # Attempt to get the database connection
except Exception as e:
    # Handle the exception (e.g., log it, raise a custom exception, etc.)
    logger.error(f"Failed to establish database connection: {e}")
    raise RuntimeError("Database connection could not be established.") from e

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()        
    try:
        yield db              
    finally:
        db.close()          