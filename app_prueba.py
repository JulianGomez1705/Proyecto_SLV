# Proyecto_SLV/app_prueba.py

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from database.database import SessionLocal, engine, Base
from database.models import Equipo_db, Jugador_db, Estadisticas_db, EstadoJugador_db
from esquemas import EquipoBase, EquipoResponse, JugadorCreate, JugadorResponse, EstadisticasBase, EstadisticasResponse, EstadoJugadorBase, EstadoJugadorResponse

Base.metadata.create_all(bind=engine)

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

@app.post("/equipos/", response_model=EquipoResponse, status_code=status.HTTP_201_CREATED)
def crear_equipo(equipo: EquipoBase, db: Session = Depends(get_db)):
    db_equipo_existente = db.query(Equipo_db).filter(Equipo_db.nombre == equipo.nombre).first()
    if db_equipo_existente:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un equipo con este nombre")

    db_equipo = Equipo_db(
        nombre=equipo.nombre,
        ubicacion=equipo.ubicacion,
        entrenador=equipo.entrenador
    )
    db.add(db_equipo)
    db.commit()
    db.refresh(db_equipo)
    return db_equipo

@app.get("/equipos/", response_model=List[EquipoResponse])
def obtener_equipos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    equipos = db.query(Equipo_db).options(joinedload(Equipo_db.jugadores)).offset(skip).limit(limit).all()
    return equipos

@app.get("/equipos/{equipo_id}", response_model=EquipoResponse)
def obtener_equipo(equipo_id: int, db: Session = Depends(get_db)):
    equipo = db.query(Equipo_db).options(joinedload(Equipo_db.jugadores)).filter(Equipo_db.id == equipo_id).first()
    if equipo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")
    return equipo

@app.put("/equipos/{equipo_id}", response_model=EquipoResponse)
def actualizar_equipo(equipo_id: int, equipo: EquipoBase, db: Session = Depends(get_db)):
    db_equipo = db.query(Equipo_db).filter(Equipo_db.id == equipo_id).first()
    if db_equipo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")

    db_equipo.nombre = equipo.nombre
    db_equipo.ubicacion = equipo.ubicacion
    db_equipo.entrenador = equipo.entrenador

    db.commit()
    db.refresh(db_equipo)
    return db_equipo

@app.delete("/equipos/{equipo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_equipo(equipo_id: int, db: Session = Depends(get_db)):
    db_equipo = db.query(Equipo_db).filter(Equipo_db.id == equipo_id).first()
    if db_equipo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")

    db.delete(db_equipo)
    db.commit()
    return {}