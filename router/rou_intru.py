# carpeta router nombre archivo rou_instru.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
# from models.models import Instrument as InstrumentModel,User as UserModel, UserInstrumentAssociation
from models.models_instru import Instrument as InstrumentSchema, InstrumentCreate
from models.modelsdb import get_db
from router.jwt_auth_users import UserDB, get_current_user
from models.models import Instrument as InstrumentModel, User as UserModel, user_instrument_association



import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

routers = APIRouter(tags=["Instrumentos"])

@routers.get("/instrumentos/{instrumento_id}", response_model=InstrumentSchema)
async def get_instrumento(instrumento_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching instrument with ID: {instrumento_id}")
    instrumento = db.query(InstrumentModel).filter(InstrumentModel.id == instrumento_id).first()
    if not instrumento:
        logger.warning(f"Instrument with ID {instrumento_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instrument not found")
    return instrumento


@routers.get("/instrumentos", response_model=List[InstrumentSchema])
async def get_instrumentos(db: Session = Depends(get_db)):
    logger.info("Fetching all instruments")
    instruments = db.query(InstrumentModel).all()
    logger.info(f"Returned {len(instruments)} instruments")
    return instruments

@routers.post("/instrumento", response_model=InstrumentSchema)
async def create_instrumento(instrumento: InstrumentCreate, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    logger.info(f"Creating new instrument for user: {current_user.username}")
    db_user = db.query(UserModel).filter(UserModel.username == current_user.username).first()
    if not db_user:
        logger.error(f"User {current_user.username} not found")
        raise HTTPException(status_code=404, detail="User not found")
    
    new_instrumento = InstrumentModel(name=instrumento.name, description=instrumento.description, price=instrumento.price)
    db.add(new_instrumento)
    db.commit()
    db.refresh(new_instrumento)
    
    association = user_instrument_association(user_id=db_user.id, instrument_id=new_instrumento.id)
    db.add(association)
    db.commit()
    db.refresh(new_instrumento)
    
    logger.info(f"New instrument created with ID: {new_instrumento.id}")
    return new_instrumento

@routers.put("/instrumento/{instrumento_id}", response_model=InstrumentSchema)
async def update_instrumento(instrumento_id: int, instrumento: InstrumentCreate, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    db_instrumento = db.query(InstrumentModel).filter(InstrumentModel.id == instrumento_id, InstrumentModel.owners.contains(current_user.id)).first()
    if not db_instrumento:
        raise HTTPException(status_code=404, detail="Instrument not found or does not belong to the current user")
    
    for key, value in instrumento.dict().items():
        setattr(db_instrumento, key, value)
    
    db.commit()
    return db_instrumento

@routers.delete("/instrumento/{instrumento_id}", response_model=InstrumentSchema)
async def delete_instrumento(instrumento_id: int, db: Session = Depends(get_db), current_user: UserDB = Depends(get_current_user)):
    db_instrumento = db.query(InstrumentModel).filter(InstrumentModel.id == instrumento_id, InstrumentModel.owners.contains(current_user.id)).first()
    if not db_instrumento:
        raise HTTPException(status_code=404, detail="Instrument not found or does not belong to the current user")
    
    db.delete(db_instrumento)
    db.commit()
    return db_instrumento
