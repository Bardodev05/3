# main.py
from fastapi import FastAPI
from models.modelsdb import engine, get_db
from models.models import Base
from router.rou_intru import routers as rou_instu

from router.jwt_auth_users import router as router_jwt_auth


# Crear tablas en la base de datos si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Instrument Management Project",
    description="CRUD and login test"
)

app.include_router(rou_instu)
app.include_router(router_jwt_auth, prefix="/jwtauth")

@app.get("/", tags=["Home"])
async def root():
    return {"message": "Welcome to the instruments API"}

