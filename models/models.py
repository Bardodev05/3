from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.declarative import declarative_base

# Definición de la clase base
Base = declarative_base()

# Tabla de asociación para la relación muchos-a-muchos
user_instrument_association = Table('user_instrument_association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('instrument_id', Integer, ForeignKey('instrumentos.id'), primary_key=True),
    extend_existing=True  # Asegúrate de que esta línea esté presente
)

# Modelo de Usuario
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    instruments = relationship("Instrument", secondary=user_instrument_association, back_populates='owners')

# Modelo de Instrumento
class Instrument(Base):
    __tablename__ = 'instrumentos'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    owners = relationship("User", secondary=user_instrument_association, back_populates='instruments')

# # Clase de asociación entre Usuario y Instrumento
# class UserInstrumentAssociation(Base):
#     __tablename__ = 'user_instrument_association'
#     user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
#     instrument_id = Column(Integer, ForeignKey('instrumentos.id'), primary_key=True)
