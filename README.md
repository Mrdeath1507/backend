# Backend - Gym Progress Tracker

Este backend está construido con FastAPI y SQLAlchemy para gestionar usuarios, entrenamientos, progreso y amistades en la aplicación Gym Progress Tracker.

## Características principales
- Registro y login de usuarios con email y nombre de usuario único
- Gestión de entrenamientos y ejercicios
- Seguimiento de progreso personal
- Sistema de amigos y solicitudes de amistad por nombre de usuario
- Comparación de progreso entre amigos
- Autenticación JWT

## Estructura de carpetas
- `main.py`: Punto de entrada de la API
- `models.py`: Modelos de base de datos (User, Workout, Friendship)
- `schemas.py`: Esquemas Pydantic para validación
- `crud.py`: Operaciones de base de datos
- `auth.py`: Lógica de autenticación y registro
- `routers/`: Rutas organizadas por funcionalidad (usuarios, entrenamientos, amigos, progreso)
- `database.py`: Configuración de la base de datos
- `requirements.txt`: Dependencias Python

## Instalación y ejecución
1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta el backend:
   ```bash
   uvicorn main:app --reload
   ```

## Endpoints principales
- `/users/register` - Registro de usuario
- `/users/login` - Login de usuario
- `/workouts/add` - Añadir entrenamiento
- `/workouts/mine` - Ver entrenamientos propios
- `/friends/request` - Solicitar amistad por nombre de usuario
- `/friends/my-friends` - Ver amigos
- `/friends/compare/{friend_id}` - Comparar progreso con amigo

## Notas
- El campo `username` es único y obligatorio para cada usuario.
- Las solicitudes de amistad y búsquedas de amigos se realizan por nombre de usuario.
- El backend está preparado para desplegarse en Railway o cualquier servicio compatible con FastAPI.

---
© 2025 Genesis CodeStudio
