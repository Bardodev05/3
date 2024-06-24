<<<<<<< HEAD
=======
# main.py
>>>>>>> b187d8137507ae62d5900483cc4c1919d781649b
from fastapi import FastAPI
from models.modelsdb import engine, get_db
from models.models import Base
from router.rou_intru import routers as rou_instu

from router.jwt_auth_users import router as router_jwt_auth


# Crear tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.title = "Proyecto de gestión de instrumentos"
app.description = "Prueba de CRUD y login"

app.include_router(rou_instu)
app.include_router(router_jwt_auth, prefix="/jwtauth")

@app.get("/", tags=["Home"])
async def root():
<<<<<<< HEAD
    return {
        "message": "Bienvenido a la API de instrumentos"
    }
=======
    return {"message": "Welcome to the instruments API"}

>>>>>>> b187d8137507ae62d5900483cc4c1919d781649b
