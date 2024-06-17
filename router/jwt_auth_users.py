# carpeta router nombre del archivo: jwt_auth_user.py
# Esto es para que el usuario esté autentificado para acceder al CRUD de instrumentos
# y los usuarios creados se van a la base de datos.

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from database import get_db
from models.models import User as UserModel
from models.models_instru import UserCreate
from sqlalchemy.orm import Session

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 30  # Duración del token de acceso en minutos
SECRET = "16a986dae60c0a57dd20122dfe2bbddeaf86dc06d1986bf145076096f3dbc5a2"

router = APIRouter(tags=["jwt_auth"])

oauth2 = OAuth2PasswordBearer(tokenUrl="jwtauth/login")
crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool = False  # Agrega el atributo 'disabled' con un valor predeterminado

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class UserDB(User):
    password: str

users_db = {
    "anderson": {
        "username": "anderson",
        "full_name": "anderson molina",
        "email": "anderosmolina123@gmail.com",
        "disabled": False,
        "password": "$2a$12$vYI1XkaJZaWdYQVjjd6jtOxFqr/V/uZDzXy5u.PiUo/gUyZpowgNO"  # Contraseña cifrada con bcrypt
    }
}

def search_user(username: str):
    if username in users_db:
        user_dict = users_db[username]
        return User(**user_dict)

# def search_user_db(username:str):
#     if username in users_db:
#         user_dict = users_db[username]
#         return UserDB(**user_dict)

def search_user_db(username: str, db: Session):
    return db.query(UserModel).filter(UserModel.username == username).first()

# async def auth_user(token: str = Depends(oauth2)):
#     exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Credenciales de autenticación inválidas",
#         headers={"WWW-Authenticate": "Bearer"}
#     )
#     try:
#         payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
#         username = payload.get("sub")
#         if username is None:
#             raise exception
#     except JWTError:
#         raise exception
#     user = search_user(username)
#     if user is None:
#         raise exception
#     return user

async def auth_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticación inválidas",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception
    user = search_user_db(username, db)
    if user is None:
        raise exception
    return user

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo"
        )
    return user

# @router.post("/login")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user_db = users_db.get(form_data.username)
#     if not user_db:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="El usuario no es correcto"
#         )
#     user = search_user_db(form_data.username)
#     if not crypt.verify(form_data.password, user.password):
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="El usuario no es correcto"
#         )
#     access_token_expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
#     access_token = jwt.encode({"sub": user.username, "exp": access_token_expires}, SECRET, algorithm=ALGORITHM)
#     return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_db = search_user_db(form_data.username, db)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no es correcto"
        )
    if not crypt.verify(form_data.password, user_db.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no es correcto"
        )
    access_token_expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
    access_token = jwt.encode({"sub": user_db.username, "exp": access_token_expires}, SECRET, algorithm=ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(current_user: User = Depends(current_user)):
    return current_user

# Nuevo endpoint para crear usuario
@router.post("/register", response_model=User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
    
    # Crear un nuevo usuario y guardar en la base de datos
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
    return new_user

@router.delete("/users/{username}")
async def delete_user(username: str, db: Session = Depends(get_db)):
    user_to_delete = db.query(UserModel).filter(UserModel.username == username).first()
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(user_to_delete)
    db.commit()
    return {"detail": f"Usuario {username} eliminado exitosamente"}


@router.patch("/users/{username}", response_model=User)
async def update_user(username: str, user_update: UserUpdate, db: Session = Depends(get_db)):
    user_to_update = db.query(UserModel).filter(UserModel.username == username).first()
    if not user_to_update:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if user_update.full_name:
        user_to_update.full_name = user_update.full_name
    if user_update.email:
        user_to_update.email = user_update.email
    if user_update.password:
        user_to_update.password = crypt.hash(user_update.password)  # Hashea la nueva contraseña
    
    db.add(user_to_update)
    db.commit()
    db.refresh(user_to_update)
    return user_to_update
