from typing import List, Optional
from pydantic import BaseModel, Field

class EquipoBase(BaseModel):
    nombre: str = Field(..., example="Los Leones")
    ubicacion: str = Field(..., example="Ciudad Deportiva")
    entrenador: str = Field(..., example="Juan Pérez")

class JugadorBase(BaseModel):
    nombre: str = Field(..., example="Carlos Gómez")
    posicion: str = Field(..., example="Delantero")
    equipo_id: Optional[int] = Field(None, example=1, description="ID del equipo al que pertenece el jugador (opcional en creación)")

class EstadisticasBase(BaseModel):
    puntosGenerales: int = Field(0, ge=0, example=150)
    puntosAtaque: int = Field(0, ge=0, example=50)
    puntosBloqueo: int = Field(0, ge=0, example=30)
    puntosSaque: int = Field(0, ge=0, example=20)
    recepcionesExitosas: int = Field(0, ge=0, example=80)
    recepcionesErradas: int = Field(0, ge=0, example=5)

class EstadoJugadorBase(BaseModel):
    alturaCm: float = Field(..., gt=0, example=185.5)
    saltoBloqueoCm: float = Field(..., ge=0, example=300.0)
    saltoAtaqueCm: float = Field(..., ge=0, example=320.0)
    lesion: Optional[str] = Field("Ninguna", example="Esguince de tobillo")

class JugadorCreate(JugadorBase):
    estadisticas: Optional[EstadisticasBase] = None
    estadoJugador: Optional[EstadoJugadorBase] = None

class EquipoForJugador(EquipoBase):
    id: int

class EstadisticasResponse(EstadisticasBase):
    id: int
    jugador_id: Optional[int] = None

    class Config:
        from_attributes = True

class EstadoJugadorResponse(EstadoJugadorBase):
    id: int
    jugador_id: Optional[int] = None

    class Config:
        from_attributes = True

class EquipoResponse(EquipoBase):
    id: int
    jugadores: List["JugadorResponse"] = []

    class Config:
        from_attributes = True

class JugadorResponse(JugadorBase):
    id: int
    equipo: Optional[EquipoForJugador] = None
    estadisticas: Optional[EstadisticasResponse] = None
    estadoJugador: Optional[EstadoJugadorResponse] = None

    class Config:
        from_attributes = True
