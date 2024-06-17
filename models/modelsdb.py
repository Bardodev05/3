# carpeta models nombre del archivo: modelsdb.py
# models/modelsdb.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base

DATABASE_URL = 'sqlite:///./test.db'  # Cambia esta URL a tu configuración de base de datos

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


