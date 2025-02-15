from sqlalchemy.orm import Session
from .database import SessionLocal  # Import SessionLocal from database.py

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()