<<<<<<< HEAD
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import users, workouts, progress, friendships

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
=======
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

>>>>>>> 706d10440f265cf7ae62f1ffaba147ebb1bd4b16
