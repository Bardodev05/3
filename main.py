from fastapi import FastAPI
from models.modelsdb import engine
from router.rou_intru import router as rou_instru
from router.jwt_auth_users import router as router_jwt_auth

# Crear las tablas en la base de datos si no existen
from models.models import Base
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.title = "Proyecto de gestión de instrumentos"
app.description = "Prueba de CRUD y login"

app.include_router(rou_instru)
app.include_router(router_jwt_auth, prefix="/jwtauth")

@app.get("/", tags=["Home"])
async def root():
    return {
        "message": "Bienvenido a la API de instrumentos"
    }
