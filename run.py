"""
Punto de entrada para Railway - importa la app de main.py
"""
import sys
import os

# Agregar el directorio actual al sys.path para que los imports funcionen
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
