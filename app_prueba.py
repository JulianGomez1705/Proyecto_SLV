from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from database.config import SessionLocal, engine, Base, obtener_sesion_bd
from database.models import Equipo_db, Jugador_db, Estadisticas_db, EstadoJugador_db
from esquemas import EquipoBase, EquipoResponse, JugadorCreate, JugadorResponse, EstadisticasBase, EstadisticasResponse, EstadoJugadorBase, EstadoJugadorResponse, EquipoForJugador

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gestión Deportiva SLV",
    description="API RESTful para la gestión de jugadores, equipos, estadísticas y estado físico.",
    version="1.0.0",
)

@app.get("/")
async def read_root():
    return {"message": "¡Bienvenido a la API de Gestión Deportiva SLV! Accede a /docs para la documentación."}

@app.post("/equipos/", response_model=EquipoResponse, status_code=status.HTTP_201_CREATED)
def crear_equipo(equipo: EquipoBase, db: Session = Depends(obtener_sesion_bd)):
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
def obtener_equipos(skip: int = 0, limit: int = 100, db: Session = Depends(obtener_sesion_bd)):
    equipos = db.query(Equipo_db).options(joinedload(Equipo_db.jugadores)).offset(skip).limit(limit).all()
    return equipos

@app.get("/equipos/{equipo_id}", response_model=EquipoResponse)
def obtener_equipo(equipo_id: int, db: Session = Depends(obtener_sesion_bd)):
    equipo = db.query(Equipo_db).options(joinedload(Equipo_db.jugadores)).filter(Equipo_db.id == equipo_id).first()
    if equipo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")
    return equipo

@app.put("/equipos/{equipo_id}", response_model=EquipoResponse)
def actualizar_equipo(equipo_id: int, equipo: EquipoBase, db: Session = Depends(obtener_sesion_bd)):
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
def eliminar_equipo(equipo_id: int, db: Session = Depends(obtener_sesion_bd)):
    db_equipo = db.query(Equipo_db).filter(Equipo_db.id == equipo_id).first()
    if db_equipo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Equipo no encontrado")

    db.delete(db_equipo)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

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