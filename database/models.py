from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Equipo_db(Base):
    __tablename__ = "equipos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    ubicacion = Column(String)
    entrenador = Column(String)
    imagen_url = Column(String, nullable=True)

    jugadores = relationship("Jugador_db", back_populates="equipo", cascade="all, delete-orphan")

class Jugador_db(Base):
    __tablename__ = "jugadores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    posicion = Column(String)
    imagen_url = Column(String, nullable=True)
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=True)

    equipo = relationship("Equipo_db", back_populates="jugadores")
    estadisticas = relationship("Estadisticas_db", back_populates="jugador", uselist=False, cascade="all, delete-orphan")
    estadoJugador = relationship("EstadoJugador_db", back_populates="jugador", uselist=False, cascade="all, delete-orphan")

class Estadisticas_db(Base):
    __tablename__ = "estadisticas"
    id = Column(Integer, primary_key=True, index=True)
    jugador_id = Column(Integer, ForeignKey("jugadores.id"), unique=True, index=True)
    puntosGenerales = Column(Integer, default=0)
    puntosAtaque = Column(Integer, default=0)
    puntosBloqueo = Column(Integer, default=0)
    puntosSaque = Column(Integer, default=0)
    recepcionesExitosas = Column(Integer, default=0)
    recepcionesErradas = Column(Integer, default=0)

    jugador = relationship("Jugador_db", back_populates="estadisticas")

class EstadoJugador_db(Base):
    __tablename__ = "estado_jugador"
    id = Column(Integer, primary_key=True, index=True)
    jugador_id = Column(Integer, ForeignKey("jugadores.id"), unique=True, index=True)
    alturaCm = Column(Float, nullable=True)
    saltoBloqueoCm = Column(Float, nullable=True)
    saltoAtaqueCm = Column(Float, nullable=True)
    lesion = Column(String, nullable=True)

    jugador = relationship("Jugador_db", back_populates="estadoJugador")
