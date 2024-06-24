from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.models_instru import Instrument as InstrumentSchema
from models.models import Instrument as InstrumentModel, User as UserModel, user_instrument_association
from router.jwt_auth_users import User, current_user

router = APIRouter()

@router.get("/instrumentos/{instrumento_id}", response_model=InstrumentSchema, tags=["Instrumentos"])
async def get_instrument_id(instrumento_id: int, db: Session = Depends(get_db), current_user: User = Depends(current_user)):
    instrumento = db.query(InstrumentModel).filter(InstrumentModel.id == instrumento_id).first()
    if not instrumento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instrumento no encontrado")
    return instrumento

@router.get("/instrumentos", response_model=List[InstrumentSchema], tags=["Instrumentos"])
async def get_instruments(db: Session = Depends(get_db), current_user: User = Depends(current_user)):
    # Accede a los instrumentos del usuario actual
    instruments = current_user.instruments
    return instruments

@router.post("/instrumento", response_model=InstrumentSchema, tags=["Instrumentos"])
async def create_instrument(instrumento: InstrumentSchema, db: Session = Depends(get_db), current_user: User = Depends(current_user)):
    instrumento_data = InstrumentModel(**instrumento.dict())
    db.add(instrumento_data)
    db.commit()
    db.refresh(instrumento_data)

    # Añadir instrumento al usuario
    current_user_db = db.query(UserModel).filter(UserModel.username == current_user.username).first()
    current_user_db.instruments.append(instrumento_data)
    db.commit()

    return instrumento_data

@router.put("/instrumentos/{instrumento_id}", response_model=InstrumentSchema, tags=["Instrumentos"])
async def update_instrumento(instrumento_id: int, instrumento: Optional[InstrumentSchema] = None, db: Session = Depends(get_db), current_user: User = Depends(current_user)):
    db_instrumento = db.query(InstrumentModel).filter(InstrumentModel.id == instrumento_id).first()
    if not db_instrumento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instrumento no encontrado")
    
    if not instrumento:  # Si no se proporcionan nuevos datos, devolver los datos actuales
        return db_instrumento

    # Si se proporcionan nuevos datos, actualizar el instrumento
    for key, value in instrumento.dict().items():
        setattr(db_instrumento, key, value)
    db.commit()
    db.refresh(db_instrumento)
    return db_instrumento

@router.delete("/instrumento/{instrumento_id}", tags=["Instrumentos"])
async def delete_instrumento(instrumento_id: int, db: Session = Depends(get_db), current_user: User = Depends(current_user)):
    instrumento = db.query(InstrumentModel).filter(InstrumentModel.id == instrumento_id).first()
    if not instrumento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instrumento no encontrado")

    # Eliminar instrumento
    db.delete(instrumento)
    db.commit()
    return {"message": "Instrumento eliminado exitosamente"}

@router.delete("/user_instrument", tags=["Relación usuario-instrumento"])
async def delete_user_instrument(user_id: int, instrument_id: int, db: Session = Depends(get_db), current_user: User = Depends(current_user)):
    # Verificar si el usuario tiene permisos adecuados para realizar esta acción
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tiene permisos para realizar esta acción")

    # Eliminar la relación entre usuario e instrumento
    association = db.execute(
        user_instrument_association.delete().where(
            (user_instrument_association.c.user_id == user_id) &
            (user_instrument_association.c.instrument_id == instrument_id)
        )
    )

    # Verificar si la relación existía
    if association.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relación usuario-instrumento no encontrada")

    db.commit()
    return {"message": "Relación usuario-instrumento eliminada exitosamente"}
