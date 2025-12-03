"""
WSGI entry point para Railway
Esto es independiente del Procfile
"""
import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
