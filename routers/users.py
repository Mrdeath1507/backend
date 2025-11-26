from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, auth

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = auth.create_user(user, db)

    # Crear token igual que en login
    access_token = auth.create_access_token({"sub": new_user.email})

    return {
        "user": {
            "id": new_user.id,
            "email": new_user.email
        },
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/login")
def login(credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    return auth.login(credentials, db)

@router.get("/me", response_model=schemas.UserResponse)
def get_current_user_data(current_user: models.User = Depends(auth.get_current_user)):
    return current_user
