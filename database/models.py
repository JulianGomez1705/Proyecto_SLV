from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base  # Importar declarative_base

# Definición de la Base declarativa para SQLAlchemy
# ESTA LÍNEA DEBE ESTAR AQUÍ UNA SOLA VEZ EN TODO EL PROYECTO.
Base = declarative_base()


class Equipo_db(Base):
    __tablename__ = "equipos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    ubicacion = Column(String)
    entrenador = Column(String)

    # Relación uno a muchos: un equipo puede tener muchos jugadores
    jugadores = relationship("Jugador_db", back_populates="equipo")


class Jugador_db(Base):
    __tablename__ = "jugadores"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    posicion = Column(String)
    # Clave foránea que referencia el id de la tabla 'equipos'
    # nullable=True permite que un jugador no tenga un equipo asignado
    equipo_id = Column(Integer, ForeignKey("equipos.id"), nullable=True)

    # Relación muchos a uno: un jugador pertenece a un equipo
    equipo = relationship("Equipo_db", back_populates="jugadores")

    # Relaciones uno a uno con Estadisticas_db y EstadoJugador_db
    # uselist=False indica una relación uno a uno
    # cascade="all, delete-orphan" asegura que si se elimina un jugador, sus estadísticas y estado también se eliminen
    estadisticas = relationship("Estadisticas_db", back_populates="jugador", uselist=False,
                                cascade="all, delete-orphan")
    estadoJugador = relationship("EstadoJugador_db", back_populates="jugador", uselist=False,
                                 cascade="all, delete-orphan")


class Estadisticas_db(Base):
    __tablename__ = "estadisticas"
    id = Column(Integer, primary_key=True, index=True)
    puntosGenerales = Column(Integer, default=0)
    puntosAtaque = Column(Integer, default=0)
    puntosBloqueo = Column(Integer, default=0)
    puntosSaque = Column(Integer, default=0)
    recepcionesExitosas = Column(Integer, default=0)
    recepcionesErradas = Column(Integer, default=0)
    # Clave foránea que referencia el id de la tabla 'jugadores'
    # unique=True asegura que solo haya un conjunto de estadísticas por jugador
    jugador_id = Column(Integer, ForeignKey("jugadores.id"), unique=True)

    # Relación uno a uno: estadísticas pertenecen a un jugador
    jugador = relationship("Jugador_db", back_populates="estadisticas")


class EstadoJugador_db(Base):
    __tablename__ = "estadousuarios"  # Nombre de tabla como se definió inicialmente
    id = Column(Integer, primary_key=True, index=True)
    alturaCm = Column(Float)
    saltoBloqueoCm = Column(Float)
    saltoAtaqueCm = Column(Float)
    lesion = Column(String, default="Ninguna")
    # Clave foránea que referencia el id de la tabla 'jugadores'
    # unique=True asegura que solo haya un estado por jugador
    jugador_id = Column(Integer, ForeignKey("jugadores.id"), unique=True)

    # Relación uno a uno: estado físico pertenece a un jugador
    jugador = relationship("Jugador_db", back_populates="estadoJugador")