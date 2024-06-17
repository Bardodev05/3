# carptea models nombre del archivo: models_instru.py
from pydantic import BaseModel
from typing import Optional

class Instrument(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    tags: Optional[dict] = None

    class Config:
        orm_mode = True

# Nuevo modelo de Pydantic para la creación de usuario
class UserCreate(BaseModel):
    username: str
    full_name: str
    email: str
    password: str