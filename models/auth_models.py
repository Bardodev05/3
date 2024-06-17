# carpeta moldes nombre del archivo auth_models.py
from pydantic import BaseModel

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

