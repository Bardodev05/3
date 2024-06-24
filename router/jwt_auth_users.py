# carpeta router nombre del archivo jwt_auth_users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from typing import Optional, List
from database import get_db
from models.auth_models import User as UserSchema, UserCreate
from models.models import User as UserModel, Instrument as InstrumentModel, user_instrument_association
from models.models_instru import Instrument as InstrumentSchema, InstrumentCreate


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 30
SECRET = "16a986dae60c0a57dd20122dfe2bbddeaf86dc06d1986bf145076096f3dbc5a2"

router = APIRouter(tags=["jwt_auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="jwtauth/login")
crypt = CryptContext(schemes=["bcrypt"])

class UserDB(BaseModel):
    username: str
    hashed_password: str
    instruments: List[InstrumentSchema] = []

    class Config:
        orm_mode = True

def get_user(username: str, db: Session):
    return db.query(UserModel).filter(UserModel.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(username, db)
    if not user or not crypt.verify(password, user.password):
        return False
    return user

def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta else datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(username, db)
    if user is None:
        raise credentials_exception
    return user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_db = authenticate_user(db, form_data.username, form_data.password)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = create_access_token(data={"sub": user_db.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserDB)
async def read_users_me(current_user: UserDB = Depends(get_current_user)):
    return current_user

@router.post("/register", response_model=UserSchema)
async def register_user(user: UserCreate, instrument: InstrumentCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
    
    hashed_password = crypt.hash(user.password)
    new_user = UserModel(
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Crear un nuevo instrumento asociado al usuario
    new_instrument = InstrumentModel(name=instrument.name, description=instrument.description, price=instrument.price)
    db.add(new_instrument)
    db.commit()
    db.refresh(new_instrument)
    
    # Asociar el instrumento al usuario
    new_user.instruments.append(new_instrument)
    db.commit()
    
    return new_user

@router.delete("/users/{username}/instruments/{instrument_id}")
async def delete_instrument(username: str, instrument_id: int, db: Session = Depends(get_db)):
    user_to_delete_from = get_user(username, db)
    if not user_to_delete_from:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    instrument_to_delete = db.query(InstrumentModel).filter(
        InstrumentModel.id == instrument_id,
        InstrumentModel.owners.contains(user_to_delete_from)
    ).first()
    if not instrument_to_delete:
        raise HTTPException(status_code=404, detail="Instrumento no encontrado o no pertenece al usuario especificado")
    
    association = db.query(user_instrument_association).filter(
        user_instrument_association.user_id == user_to_delete_from.id,
        user_instrument_association.instrument_id == instrument_id
    ).first()
    
    db.delete(association)
    db.commit()
    return {"detail": f"Instrumento {instrument_id} eliminado exitosamente del usuario {username}"}

@router.put("/users/{username}/instruments/{instrument_id}")
async def update_instrument(username: str, instrument_id: int, instrument_update: InstrumentCreate, db: Session = Depends(get_db)):
    user_to_update_from = get_user(username, db)
    if not user_to_update_from:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    instrument_to_update = db.query(InstrumentModel).filter(
        InstrumentModel.id == instrument_id,
        InstrumentModel.owners.contains(user_to_update_from)
    ).first()
    if not instrument_to_update:
        raise HTTPException(status_code=404, detail="Instrumento no encontrado o no pertenece al usuario especificado")
    
    instrument_to_update.name = instrument_update.name
    instrument_to_update.description = instrument_update.description
    instrument_to_update.price = instrument_update.price
    
    association = db.query(user_instrument_association).filter(
        user_instrument_association.user_id == user_to_update_from.id,
        user_instrument_association.instrument_id == instrument_id
    ).first()
    
    db.commit()
    return {"detail": f"Instrumento {instrument_id} actualizado exitosamente para el usuario {username}"}
