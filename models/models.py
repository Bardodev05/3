# carpeta models nombre del archivo: models.py
# aca deben de guardase los instrumentos y los usuarios
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    disabled = Column(Boolean, default=False)
    password = Column(String)
    
    instruments = relationship("Instrument", back_populates="owner")

class Instrument(Base):
    __tablename__ = 'instrumentos'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    tags = Column(JSON)

    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="instruments")

