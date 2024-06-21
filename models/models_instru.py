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
        # arbitrary_types_allowed = True
