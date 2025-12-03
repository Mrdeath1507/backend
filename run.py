"""
Punto de entrada para Railway - importa la app de main.py
"""
import sys
import os

# Agregar el directorio actual al sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print(f"Current directory: {current_dir}")
print(f"sys.path: {sys.path}")
print(f"Files in directory: {os.listdir(current_dir)}")

try:
    from main import app
    print("✓ Successfully imported app from main.py")
except ImportError as e:
    print(f"✗ Failed to import app: {e}")
    raise

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
