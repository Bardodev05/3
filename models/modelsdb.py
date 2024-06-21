# carpeta models nombre del archivo modelsdb.py
from sqlalchemy import create_engine, Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Configuración de la base de datos
DATABASE_URL = "sqlite:///./test.db"  # Cambia esto por la URL de tu base de datos

engine = create_engine(DATABASE_URL, future=True, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definición de la clase base
Base = declarative_base()

# Ahora puedes importar Base desde models.models si es necesario para otras partes de tu código
from models.models import Base

# Función para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
