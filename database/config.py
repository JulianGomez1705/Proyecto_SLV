from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# ¡Tu "External Database URL" de Render PostgreSQL pegada aquí!
SQLALCHEMY_DATABASE_URL = "postgresql://proyecto_superliga_db_user:XqMuKEs4rkn1cqTWNcHGdGCzDWYbHAzc@dpg-d13nmcodl3ps7391vv6g-a.oregon-postgres.render.com/proyecto_superliga_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def obtener_sesion_bd():
    sesion_bd = SessionLocal()
    try:
        yield sesion_bd
    finally:
        sesion_bd.close()
