# En tu archivo de modelos (auth_models.py)
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

Base = declarative_base()

# Tabla de asociación
user_instrument_association = Table(
    'user_instrument', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('instrument_id', Integer, ForeignKey('instrumentos.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    disabled = Column(Boolean, default=False)
    password = Column(String)

    instruments = relationship("Instrument", secondary=user_instrument_association, back_populates="users")

class Instrument(Base):
    __tablename__ = 'instrumentos'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    tags = Column(JSON)

    users = relationship("User", secondary=user_instrument_association, back_populates="instruments")
