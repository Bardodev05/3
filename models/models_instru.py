from pydantic import BaseModel
from typing import Optional, List

# Define InstrumentBase as the base model for instrument-related models
class InstrumentBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

# Use InstrumentBase for creating new instruments
class InstrumentCreate(InstrumentBase):
    pass

# Define Instrument as a separate model that includes an ID, inheriting from InstrumentBase
class Instrument(InstrumentBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True
<<<<<<< HEAD

class UserCreate(BaseModel):
    username: str
    full_name: str
    email: str
    password: str

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool
    instruments: Optional[List[Instrument]] = []

    class Config:
        orm_mode = True
=======
        # arbitrary_types_allowed = True
>>>>>>> b187d8137507ae62d5900483cc4c1919d781649b
