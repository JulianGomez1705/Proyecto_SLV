from typing import List, Optional
from pydantic import BaseModel, Field

class EstadisticasBase(BaseModel):
    puntosGenerales: Optional[int] = 0
    puntosAtaque: Optional[int] = 0
    puntosBloqueo: Optional[int] = 0
    puntosSaque: Optional[int] = 0
    recepcionesExitosas: Optional[int] = 0
    recepcionesErradas: Optional[int] = 0

class EstadisticasCreate(EstadisticasBase):
    pass

class EstadisticasResponse(EstadisticasBase):
    id: int
    jugador_id: int

    class Config:
        from_attributes = True

class EstadoJugadorBase(BaseModel):
    alturaCm: Optional[float] = None
    saltoBloqueoCm: Optional[float] = None
    saltoAtaqueCm: Optional[float] = None
    lesion: Optional[str] = None

class EstadoJugadorCreate(EstadoJugadorBase):
    pass

class EstadoJugadorResponse(EstadoJugadorBase):
    id: int
    jugador_id: int

    class Config:
        from_attributes = True

class EquipoForJugador(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True

class JugadorBase(BaseModel):
    nombre: str
    posicion: str
    imagen_url: Optional[str] = None

class JugadorCreate(JugadorBase):
    equipo_id: Optional[int] = None
    estadisticas: Optional[EstadisticasCreate] = None
    estadoJugador: Optional[EstadoJugadorCreate] = None

class JugadorResponse(JugadorBase):
    id: int
    equipo_id: Optional[int] = None
    equipo: Optional[EquipoForJugador] = None
    estadisticas: Optional[EstadisticasResponse] = None
    estadoJugador: Optional[EstadoJugadorResponse] = None

    class Config:
        from_attributes = True

class EquipoBase(BaseModel):
    nombre: str
    ubicacion: str
    entrenador: str

class EquipoCreate(EquipoBase):
    pass

class EquipoResponse(EquipoBase):
    id: int
    jugadores: List[JugadorResponse] = []

    class Config:
        from_attributes = True
