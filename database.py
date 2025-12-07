import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Si no hay DATABASE_URL en el entorno o está vacía, usar un SQLite local de fallback (solo para desarrollo)
if not DATABASE_URL:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sqlite_path = os.path.join(current_dir, "dev_database.db")
    DATABASE_URL = f"sqlite:///{sqlite_path}"
    print(f"[database.py] WARNING: DATABASE_URL no definida. Usando fallback SQLite en {sqlite_path}")
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
