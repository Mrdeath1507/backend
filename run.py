"""
Punto de entrada para Railway - importa la app de main.py
"""
from main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
