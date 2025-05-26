

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Jugador_db(Base):
    __tablename__ = "jugadores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    posicion = Column(String, nullable=False)

    estadisticas = relationship("Estadisticas_db", back_populates="jugador", uselist=False)
    estadoJugador = relationship("EstadoJugador_db", back_populates="jugador", uselist=False)

    equipo_id = Column(Integer, ForeignKey("equipos.id"))
    equipo = relationship("Equipo_db", back_populates="jugadores")


class Equipo_db(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True, nullable=False)
    ubicacion = Column(String, nullable=False)
    entrenador = Column(String, nullable=False)

    jugadores = relationship("Jugador_db", back_populates="equipo")


class Estadisticas_db(Base):
    __tablename__ = "estadisticas"

    id = Column(Integer, primary_key=True, index=True)
    puntosGenerales = Column(Integer, default=0)
    puntosAtaque = Column(Integer, default=0)
    puntosBloqueo = Column(Integer, default=0)
    puntosSaque = Column(Integer, default=0)
    recepcionesExitosas = Column(Integer, default=0)
    recepcionesErradas = Column(Integer, default=0)

    jugador_id = Column(Integer, ForeignKey("jugadores.id"), unique=True)
    jugador = relationship("Jugador_db", back_populates="estadisticas")


class EstadoJugador_db(Base):
    __tablename__ = "estado_jugador"

    id = Column(Integer, primary_key=True, index=True)
    alturaCm = Column(Float, nullable=False)
    saltoBloqueoCm = Column(Float, nullable=False)
    saltoAtaqueCm = Column(Float, nullable=False)
    lesion = Column(String, default="Ninguna")

    jugador_id = Column(Integer, ForeignKey("jugadores.id"), unique=True)
    jugador = relationship("Jugador_db", back_populates="estadoJugador")