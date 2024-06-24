# nombre del archivo database.py
from sqlalchemy.orm import Session
from models.modelsdb import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
