from pydantic import BaseModel
from typing import Optional, List

class Instrument(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    tags: Optional[dict] = None

    class Config:
        orm_mode = True

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
