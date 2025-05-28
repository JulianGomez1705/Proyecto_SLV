from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session, joinedload

from .database.config import obtener_sesion_bd
from .database.models import Equipo_db, Jugador_db, Estadisticas_db, EstadoJugador_db
from .esquemas import (
    EquipoCreate, EquipoResponse,
    JugadorCreate, JugadorBase, JugadorResponse,
    EstadisticasBase, EstadisticasResponse,
    EstadoJugadorBase, EstadoJugadorResponse,
    EquipoForJugador
)

app = FastAPI()

# --- ENDPOINTS PARA EQUIPOS ---

@app.post("/equipos/", response_model=EquipoResponse, status_code=status.HTTP_201_CREATED)
def crear_equipo(datos_equipo: EquipoCreate, sesion_bd: Session = Depends(obtener_sesion_bd)):
    nuevo_equipo_bd = Equipo_db(**datos_equipo.model_dump())
    sesion_bd.add(nuevo_equipo_bd)
    sesion_bd.commit()
    sesion_bd.refresh(nuevo_equipo_bd)
    return nuevo_equipo_bd

@app.get("/equipos/", response_model=List[EquipoResponse], status_code=status.HTTP_200_OK)
def obtener_equipos(
    sesion_bd: Session = Depends(obtener_sesion_bd),
    skip: int = 0,
    limit: int = 100
):
    equipos = sesion_bd.query(Equipo_db).offset(skip).limit(limit).all()
    return equipos

@app.get("/equipos/{equipo_id}", response_model=EquipoResponse, status_code=status.HTTP_200_OK)
def obtener_equipo_por_id(equipo_id: int, sesion_bd: Session = Depends(obtener_sesion_bd)):
    equipo = sesion_bd.query(Equipo_db).filter(Equipo_db.id == equipo_id).first()
    if not equipo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")
    return equipo

@app.put("/equipos/{equipo_id}", response_model=EquipoResponse, status_code=status.HTTP_200_OK)
def actualizar_equipo(equipo_id: int, datos_actualizacion: EquipoCreate, sesion_bd: Session = Depends(obtener_sesion_bd)):
    equipo_existente = sesion_bd.query(Equipo_db).filter(Equipo_db.id == equipo_id).first()
    if not equipo_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")

    for campo, valor in datos_actualizacion.model_dump(exclude_unset=True).items():
        setattr(equipo_existente, campo, valor)

    sesion_bd.add(equipo_existente)
    sesion_bd.commit()
    sesion_bd.refresh(equipo_existente)
    return equipo_existente

@app.delete("/equipos/{equipo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_equipo(equipo_id: int, sesion_bd: Session = Depends(obtener_sesion_bd)):
    equipo = sesion_bd.query(Equipo_db).filter(Equipo_db.id == equipo_id).first()
    if not equipo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")

    sesion_bd.delete(equipo)
    sesion_bd.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# --- ENDPOINTS PARA JUGADORES ---

@app.post("/jugadores/", response_model=JugadorResponse, status_code=status.HTTP_201_CREATED)
def crear_jugador(datos_jugador: JugadorCreate, sesion_bd: Session = Depends(obtener_sesion_bd)):
    if datos_jugador.equipo_id:
        equipo_bd = sesion_bd.query(Equipo_db).filter(Equipo_db.id == datos_jugador.equipo_id).first()
        if not equipo_bd:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")

    nuevo_jugador_bd = Jugador_db(
        nombre=datos_jugador.nombre,
        posicion=datos_jugador.posicion,
        equipo_id=datos_jugador.equipo_id
    )

    if datos_jugador.estadisticas:
        estadisticas_bd = Estadisticas_db(**datos_jugador.estadisticas.model_dump())
        nuevo_jugador_bd.estadisticas = estadisticas_bd

    if datos_jugador.estadoJugador:
        estado_jugador_bd = EstadoJugador_db(**datos_jugador.estadoJugador.model_dump())
        nuevo_jugador_bd.estadoJugador = estado_jugador_bd

    sesion_bd.add(nuevo_jugador_bd)
    sesion_bd.commit()
    sesion_bd.refresh(nuevo_jugador_bd)

    nuevo_jugador_bd = sesion_bd.query(Jugador_db).options(
        joinedload(Jugador_db.equipo),
        joinedload(Jugador_db.estadisticas),
        joinedload(Jugador_db.estadoJugador)
    ).filter(Jugador_db.id == nuevo_jugador_bd.id).first()

    return nuevo_jugador_bd

@app.get("/jugadores/", response_model=List[JugadorResponse], status_code=status.HTTP_200_OK)
def obtener_jugadores(
    sesion_bd: Session = Depends(obtener_sesion_bd),
    skip: int = 0,
    limit: int = 100
):
    jugadores = sesion_bd.query(Jugador_db).options(
        joinedload(Jugador_db.equipo),
        joinedload(Jugador_db.estadisticas),
        joinedload(Jugador_db.estadoJugador)
    ).offset(skip).limit(limit).all()
    return jugadores

@app.get("/jugadores/{jugador_id}", response_model=JugadorResponse, status_code=status.HTTP_200_OK)
def obtener_jugador_por_id(jugador_id: int, sesion_bd: Session = Depends(obtener_sesion_bd)):
    jugador = sesion_bd.query(Jugador_db).options(
        joinedload(Jugador_db.equipo),
        joinedload(Jugador_db.estadisticas),
        joinedload(Jugador_db.estadoJugador)
    ).filter(Jugador_db.id == jugador_id).first()

    if not jugador:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador no encontrado")
    return jugador

@app.put("/jugadores/{jugador_id}", response_model=JugadorResponse, status_code=status.HTTP_200_OK)
def actualizar_jugador(jugador_id: int, datos_actualizacion: JugadorCreate, sesion_bd: Session = Depends(obtener_sesion_bd)):
    jugador_existente = sesion_bd.query(Jugador_db).options(
        joinedload(Jugador_db.estadisticas),
        joinedload(Jugador_db.estadoJugador)
    ).filter(Jugador_db.id == jugador_id).first()

    if not jugador_existente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador no encontrado")

    if datos_actualizacion.equipo_id is not None:
        equipo_bd = sesion_bd.query(Equipo_db).filter(Equipo_db.id == datos_actualizacion.equipo_id).first()
        if not equipo_bd:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")

    for campo, valor in datos_actualizacion.model_dump(exclude_unset=True, exclude={'estadisticas', 'estadoJugador'}).items():
        setattr(jugador_existente, campo, valor)

    if datos_actualizacion.estadisticas:
        if jugador_existente.estadisticas:
            for campo, valor in datos_actualizacion.estadisticas.model_dump(exclude_unset=True).items():
                setattr(jugador_existente.estadisticas, campo, valor)
        else:
            estadisticas_bd = Estadisticas_db(**datos_actualizacion.estadisticas.model_dump())
            jugador_existente.estadisticas = estadisticas_bd

    if datos_actualizacion.estadoJugador:
        if jugador_existente.estadoJugador:
            for campo, valor in datos_actualizacion.estadoJugador.model_dump(exclude_unset=True).items():
                setattr(jugador_existente.estadoJugador, campo, valor)
        else:
            estado_jugador_bd = EstadoJugador_db(**datos_actualizacion.estadoJugador.model_dump())
            jugador_existente.estadoJugador = estado_jugador_bd

    sesion_bd.add(jugador_existente)
    sesion_bd.commit()
    sesion_bd.refresh(jugador_existente)

    jugador_existente = sesion_bd.query(Jugador_db).options(
        joinedload(Jugador_db.equipo),
        joinedload(Jugador_db.estadisticas),
        joinedload(Jugador_db.estadoJugador)
    ).filter(Jugador_db.id == jugador_id).first()

    return jugador_existente

@app.delete("/jugadores/{jugador_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_jugador(jugador_id: int, sesion_bd: Session = Depends(obtener_sesion_bd)):
    jugador = sesion_bd.query(Jugador_db).filter(Jugador_db.id == jugador_id).first()

    if not jugador:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador no encontrado")

    sesion_bd.delete(jugador)
    sesion_bd.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)