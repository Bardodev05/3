# En models/auth_models.py

from typing import Optional, List
from pydantic import BaseModel, EmailStr
from models.models import Instrument
from models.models_instru import InstrumentCreate

class UserBase(BaseModel):
    username: str
    full_name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    instruments: Optional[List['InstrumentCreate']] = None

class User(UserBase):
    id: int
    instruments: List['Instrument'] = []

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True



