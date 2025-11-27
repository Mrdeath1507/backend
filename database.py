import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar variables del entorno (.env en local, Environment Variables en Render)
load_dotenv()

# Leer DATABASE_URL desde variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise ValueError("❌ DATABASE_URL no está definida en las variables de entorno")

# Render exige SSL
DATABASE_URL = DATABASE_URL + "?sslmode=require"

# Crear engine
engine = create_engine(DATABASE_URL)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base de modelos
Base = declarative_base()

# Dependencia de FastAPI para obtener sesión de BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
