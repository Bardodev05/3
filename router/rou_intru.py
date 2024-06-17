# carpeta router nombre del archivo:rou_instru,py
# la idea es que se debe de autentificar para acceder al crud
# los isntrumentos deden de ir ala base de datos
# y los usuarios autentidicados tamnien
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.models_instru import Instrument as InstrumentSchema
from models.models import Instrument as InstrumentModel
from router.jwt_auth_users import User, current_user

router = APIRouter()

@router.get("/instrumentos/{instrumento_id}", response_model=InstrumentSchema,tags=["Intrumentos"])
async def get_instrument_id(instrumento_id: int, db: Session = Depends(get_db), current_user: User = Depends(current_user)):
    instrumento = db.query(InstrumentModel).filter(InstrumentModel.id == instrumento_id).first()
    if not instrumento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instrumento no encontrado")
    return instrumento

@router.get("/instrumentos", response_model=List[InstrumentSchema],tags=["Intrumentos"])
async def get_instruments(db: Session = Depends(get_db), current_user: User = Depends(current_user)):
    return db.query(InstrumentModel).all()

@router.post("/instrumento", response_model=InstrumentSchema, tags=["Intrumentos"])
async def create_instrument(instrumento: InstrumentSchema, db: Session = Depends(get_db), current_user: User = Depends(current_user)):
    instrumento_data = InstrumentModel(**instrumento.dict())
    db.add(instrumento_data)
    db.commit()
    db.refresh(instrumento_data)
    return instrumento_data

@router.put("/instrumentos/{instrumento_id}", response_model=InstrumentSchema,tags=["Intrumentos"])
async def update_instrumento(instrumento_id: int, instrumento: InstrumentSchema, db: Session = Depends(get_db), current_user: User = Depends(current_user)):
    db_instrumento = db.query(InstrumentModel).filter(InstrumentModel.id == instrumento_id).first()
    if not db_instrumento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instrumento no encontrado")
    for key, value in instrumento.dict().items():
        setattr(db_instrumento, key, value)
    db.commit()
    db.refresh(db_instrumento)
    return db_instrumento

@router.delete("/instrumento/{instrumento_id}",tags=["Intrumentos"])
async def delete_instrumento(instrumento_id: int, db: Session = Depends(get_db), current_user: User = Depends(current_user)):
    instrumento = db.query(InstrumentModel).filter(InstrumentModel.id == instrumento_id).first()
    if not instrumento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instrumento no encontrado")
    db.delete(instrumento)
    db.commit()
    return {"message": "Instrumento eliminado exitosamente"}
