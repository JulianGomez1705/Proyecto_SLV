from typing import List, Optional
from pydantic import BaseModel

class EquipoBase(BaseModel):
    nombre: str
    ubicacion: str
    entrenador: str

class EstadisticasBase(BaseModel):
    puntosGenerales: int
    puntosAtaque: int
    puntosBloqueo: int
    puntosSaque: int
    recepcionesExitosas: int
    recepcionesErradas: int

class EstadoJugadorBase(BaseModel):
    alturaCm: float
    saltoBloqueoCm: float
    saltoAtaqueCm: float
    lesion: Optional[str] = None

class JugadorBase(BaseModel):
    nombre: str
    posicion: str
    equipo_id: Optional[int] = None

class JugadorCreate(JugadorBase):
    estadisticas: Optional[EstadisticasBase] = None
    estadoJugador: Optional[EstadoJugadorBase] = None

class EquipoForJugador(EquipoBase):
    id: int

class EstadisticasResponse(EstadisticasBase):
    id: int
    jugador_id: Optional[int] = None

class EstadoJugadorResponse(EstadoJugadorBase):
    id: int
    jugador_id: Optional[int] = None

class JugadorResponse(JugadorBase):
    id: int
    equipo: Optional[EquipoForJugador] = None
    estadisticas: Optional[EstadisticasResponse] = None
    estadoJugador: Optional[EstadoJugadorResponse] = None

class EquipoResponse(EquipoBase):
    id: int
    jugadores: List[JugadorResponse] = []

