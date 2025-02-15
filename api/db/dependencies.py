from sqlalchemy.orm import Session
from .database import SessionLocal  # Import from your existing database.py

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()