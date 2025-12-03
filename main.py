from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import sys
import os
from datetime import datetime

print(f"[main.py] Current working directory: {os.getcwd()}")
print(f"[main.py] sys.path: {sys.path}")

from database import Base, engine
from routers import users, workouts, progress, friendships

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gym Progress API",
    version="1.0.2"
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

# ==================== SISTEMA DE ACTUALIZACIONES ====================

# Versión actual de la app
CURRENT_APP_VERSION = "1.0.1"
LAST_UPDATE_DATE = "2025-12-03"

@app.get("/api/version")
def get_version():
    """
    Endpoint para verificar versión disponible de la app
    
    Respuesta:
    {
        "version": "1.0.1",
        "installed_version": "1.0.0",  # La que el usuario tiene
        "update_available": true,
        "changelog": "...",
        "download_url": "https://...",  # URL del APK
        "required": false,  # Si true, fuerza actualización
        "release_date": "2025-12-03"
    }
    """
    return {
        "version": CURRENT_APP_VERSION,
        "update_available": True,
        "changelog": "✅ Entrenamientos se guardan correctamente\n✅ Corrección del manifest.json\n✅ Sistema de actualizaciones automáticas",
        "required": False,
        "release_date": LAST_UPDATE_DATE,
        "last_check": datetime.now().isoformat()
    }

@app.post("/api/check-update")
async def check_update(data: dict):
    """
    Verificar si hay actualización disponible
    Recibe: {"current_version": "1.0.0"}
    """
    try:
        current_version = data.get("current_version", "0.0.0")
        
        # Comparar versiones
        is_update_available = compare_versions(CURRENT_APP_VERSION, current_version) > 0
        
        return {
            "update_available": is_update_available,
            "latest_version": CURRENT_APP_VERSION,
            "current_version": current_version,
            "message": "Nueva versión disponible" if is_update_available else "Ya tienes la última versión",
            "changelog": "✅ Entrenamientos se guardan correctamente\n✅ Corrección del manifest.json\n✅ Sistema de actualizaciones automáticas"
        }
    except Exception as e:
        return {"error": str(e), "update_available": False}

def compare_versions(v1, v2):
    """Compara dos versiones semánticas. Retorna 1 si v1>v2, -1 si v1<v2, 0 si son iguales"""
    try:
        parts1 = list(map(int, v1.split('.')))
        parts2 = list(map(int, v2.split('.')))
        
        for i in range(max(len(parts1), len(parts2))):
            p1 = parts1[i] if i < len(parts1) else 0
            p2 = parts2[i] if i < len(parts2) else 0
            
            if p1 > p2:
                return 1
            elif p1 < p2:
                return -1
        return 0
    except:
        return 0
