from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

print(f"[main.py] Current working directory: {os.getcwd()}")
print(f"[main.py] sys.path: {sys.path}")

from database import Base, engine
from routers import users, workouts, progress, friendships

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gym Progress API",
    version="1.0.0"
)

# CORS PARA APP WEB + ANDROID
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(workouts.router)
app.include_router(progress.router)
app.include_router(friendships.router)

@app.get("/")
def root():
    return {"status": "API Online", "message": "Gym Progress API funcionando en producción 🚀"}

@app.get("/api/version")
def get_version():
    """Endpoint para verificar versión disponible de la app"""
    # La versión puede ser actualizada aquí o desde una variable de entorno
    return {
        "version": "1.0.1",  # Cambiar esto cuando haya una nueva versión
        "changelog": "- Ahorro de entrenamientos corregido\n- Mejoras de rendimiento",
        "required": False  # Si es True, fuerza actualización
    }
