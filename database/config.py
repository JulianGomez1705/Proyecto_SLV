from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 'Base' ya NO se define aquí. Se definirá en database/models.py

def obtener_sesion_bd():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()