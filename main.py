# Proyecto_SLV/main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database.database import SessionLocal, engine, Base
from database import models as db_models


db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gestión Deportiva SLV",
    description="API RESTful para la gestión de jugadores, equipos, estadísticas y estado físico.",
    version="1.0.0",
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():
    return {"message": "¡Bienvenido a la API de Gestión Deportiva SLV! Accede a /docs para la documentación."}