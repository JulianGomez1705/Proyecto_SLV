from typing import List, Optional
from pydantic import BaseModel, Field

# Esquemas para Estadisticas
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

# Esquemas para EstadoJugador
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

# Esquema para Equipo (para que JugadorResponse pueda referenciarlo)
class EquipoForJugador(BaseModel):
    id: int
    nombre: str
    # Incluimos la imagen_url también aquí para que se cargue cuando se obtiene un jugador
    imagen_url: Optional[str] = None

    class Config:
        from_attributes = True

# Esquemas para Jugador
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

# Esquemas para Equipo
class EquipoBase(BaseModel):
    nombre: str
    ubicacion: str
    entrenador: str
    # Nuevo campo para la URL de la imagen del equipo
    imagen_url: Optional[str] = None

class EquipoCreate(EquipoBase):
    pass

class EquipoResponse(EquipoBase):
    id: int
    # Los jugadores dentro de EquipoResponse también necesitan el campo imagen_url
    jugadores: List[JugadorResponse] = []

    class Config:
        from_attributes = True
