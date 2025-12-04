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


@app.get("/mgp/version.json")
async def mgp_version():
    """
    Endpoint simple que retorna el JSON de versión para OTA externo.
    Ejemplo disponible en: https://<tu-dominio>/mgp/version.json
    """
    try:
        # Datos de ejemplo; actualiza aquí cuando publiques un APK nuevo
        data = {
            "latestVersionName": "1.1.0",
            "latestVersionCode": 2,
            "apkUrl": "https://web-production-2f216.up.railway.app/mgp/MyGymProgress-1.1.0.apk",
            "changelog": "• Nuevo sistema de progreso.\n• Corrección de errores.\n• Mejoras de rendimiento."
        }
        return data
    except Exception as e:
        return {"error": str(e)}

# ==================== SISTEMA DE ACTUALIZACIONES ====================

# Versión actual de la app
CURRENT_APP_VERSION = "1.0.2"
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
    Recibe: {"current_version": "1.0.0", "platform": "android", "app_id": "..."}
    """
    try:
        current_version = data.get("current_version", "0.0.0")
        platform = data.get("platform", "web")
        
        # Comparar versiones
        is_update_available = compare_versions(CURRENT_APP_VERSION, current_version) > 0
        
        response = {
            "update_available": is_update_available,
            "latest_version": CURRENT_APP_VERSION,
            "current_version": current_version,
            "changelog": "✅ Entrenamientos se guardan correctamente\n✅ Corrección del manifest.json\n✅ Sistema de actualizaciones automáticas",
            "release_date": LAST_UPDATE_DATE
        }
        
        # Si es Android, agregar URL de descarga
        if platform == "android" and is_update_available:
            response["download_url"] = f"https://web-production-2f216.up.railway.app/api/download-update/{CURRENT_APP_VERSION}"
        
        return response
        
    except Exception as e:
        return {"error": str(e), "update_available": False}

@app.get("/api/download-update/{version}")
async def download_update(version: str, file: str = None):
    """
    Endpoint para descargar archivos específicos de la actualización
    
    Parámetros:
    - version: versión a descargar (ej: 1.0.2)
    - file: archivo específico a descargar (ej: js/api.js)
    
    En producción, aquí se servirían los archivos actualizados desde un repositorio
    o servidor de archivos.
    
    Para desarrollo, retorna los archivos locales del proyecto.
    """
    try:
        # Verificar que la versión es válida
        if not is_valid_version(version):
            return {"error": "Versión inválida"}
        
        # Si piden un archivo específico
        if file:
            # Ruta base del proyecto frontend
            frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "www", file)
            
            # Sanitizar path para evitar traversal attacks
            frontend_path = os.path.abspath(frontend_path)
            base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "www"))
            
            if not frontend_path.startswith(base_path):
                return {"error": "Path inválido"}
            
            if os.path.isfile(frontend_path):
                return FileResponse(frontend_path, media_type="text/plain")
            else:
                return {"error": f"Archivo no encontrado: {file}"}
        
        # Si no especifica archivo, retornar información de actualización
        return {
            "status": "ok",
            "version": version,
            "message": "Actualización disponible para descargar",
            "size_mb": 0.5,
            "checksum": "abc123def456",
            "files": [
                "js/api.js",
                "js/dashboard.js",
                "js/auth.js",
                "css/style.css",
                "dashboard.html",
                "index.html"
            ]
        }
    except Exception as e:
        return {"error": str(e)}

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

def is_valid_version(version: str) -> bool:
    """Verifica que la versión tenga formato válido (X.Y.Z)"""
    try:
        parts = version.split('.')
        return len(parts) == 3 and all(p.isdigit() for p in parts)
    except:
        return False
