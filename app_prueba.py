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

def obtener_sesion_bd():
    sesion_bd = SessionLocal()
    try:
        yield sesion_bd
    finally:
        sesion_bd.close()

@app.get("/")
async def leer_raiz():
    return {"mensaje": "¡Bienvenido a la API de Gestión Deportiva SLV! Accede a /docs para la documentación."}

@app.post("/equipos/", response_model=EquipoResponse, status_code=status.HTTP_201_CREATED)
def crear_equipo(datos_equipo: EquipoBase, sesion_bd: Session = Depends(obtener_sesion_bd)):
    equipo_existente_bd = sesion_bd.query(Equipo_db).filter(Equipo_db.nombre == datos_equipo.nombre).first()
    if equipo_existente_bd:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un equipo con este nombre")

    nuevo_equipo_bd = Equipo_db(
        nombre=datos_equipo.nombre,
        ubicacion=datos_equipo.ubicacion,
        entrenador=datos_equipo.entrenador
    )
    sesion_bd.add(nuevo_equipo_bd)
    sesion_bd.commit()
    sesion_bd.refresh(nuevo_equipo_bd)
    return nuevo_equipo_bd

@app.get("/equipos/", response_model=List[EquipoResponse])
def obtener_equipos(saltar: int = 0, limite: int = 100, sesion_bd: Session = Depends(obtener_sesion_bd)):
    lista_equipos = sesion_bd.query(Equipo_db).options(joinedload(Equipo_db.jugadores)).offset(saltar).limit(limite).all()
    return lista_equipos

@app.get("/equipos/{id_equipo}", response_model=EquipoResponse)
def obtener_equipo_por_id(id_equipo: int, sesion_bd: Session = Depends(obtener_sesion_bd)):
    equipo_bd = sesion_bd.query(Equipo_db).options(joinedload(Equipo_db.jugadores)).filter(Equipo_db.id == id_equipo).first()
    if equipo_bd is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")
    return equipo_bd

@app.put("/equipos/{id_equipo}", response_model=EquipoResponse)
def actualizar_equipo(id_equipo: int, datos_equipo: EquipoBase, sesion_bd: Session = Depends(obtener_sesion_bd)):
    equipo_bd = sesion_bd.query(Equipo_db).filter(Equipo_db.id == id_equipo).first()
    if equipo_bd is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")

    equipo_bd.nombre = datos_equipo.nombre
    equipo_bd.ubicacion = datos_equipo.ubicacion
    equipo_bd.entrenador = datos_equipo.entrenador

    sesion_bd.commit()
    sesion_bd.refresh(equipo_bd)
    return equipo_bd

@app.delete("/equipos/{id_equipo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_equipo(id_equipo: int, sesion_bd: Session = Depends(obtener_sesion_bd)):
    equipo_bd = sesion_bd.query(Equipo_db).filter(Equipo_db.id == id_equipo).first()
    if equipo_bd is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")

    sesion_bd.delete(equipo_bd)
    sesion_bd.commit()
    return {}