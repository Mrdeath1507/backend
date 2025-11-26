from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from import models, schemas, auth

router = APIRouter(
    prefix="/friends",
    tags=["Friends"]
)


@router.post("/request", response_model=schemas.FriendshipResponse)
def send_friend_request(
    friendship: schemas.FriendshipCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Buscar al usuario amigo por email
    friend_user = db.query(models.User).filter(models.User.email == friendship.friend_email).first()
    
    if not friend_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if friend_user.id == current_user.id:
        raise HTTPException(status_code=400, detail="No puedes agregarte a ti mismo")
    
    # Verificar si ya existe una solicitud
    existing_request = db.query(models.Friendship).filter(
        ((models.Friendship.user_id == current_user.id) & (models.Friendship.friend_id == friend_user.id)) |
        ((models.Friendship.user_id == friend_user.id) & (models.Friendship.friend_id == current_user.id))
    ).first()
    
    if existing_request:
        raise HTTPException(status_code=400, detail="Ya existe una solicitud de amistad")
    
    # Crear nueva solicitud
    new_friendship = models.Friendship(
        user_id=current_user.id,
        friend_id=friend_user.id,
        status="pending"
    )
    
    db.add(new_friendship)
    db.commit()
    db.refresh(new_friendship)
    
    return {
        "id": new_friendship.id,
        "user_id": new_friendship.user_id,
        "friend_id": new_friendship.friend_id,
        "status": new_friendship.status,
        "friend_email": friend_user.email,
        "friend_name": friend_user.email.split('@')[0]
    }

@router.get("/requests", response_model=List[schemas.FriendshipResponse])
def get_friend_requests(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    requests = db.query(models.Friendship).filter(
        models.Friendship.friend_id == current_user.id,
        models.Friendship.status == "pending"
    ).all()
    
    result = []
    for request in requests:
        friend_user = db.query(models.User).filter(models.User.id == request.user_id).first()
        result.append({
            "id": request.id,
            "user_id": request.user_id,
            "friend_id": request.friend_id,
            "status": request.status,
            "friend_email": friend_user.email,
            "friend_name": friend_user.email.split('@')[0]
        })
    
    return result

@router.post("/accept/{request_id}")
def accept_friend_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    friendship = db.query(models.Friendship).filter(
        models.Friendship.id == request_id,
        models.Friendship.friend_id == current_user.id,
        models.Friendship.status == "pending"
    ).first()
    
    if not friendship:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    
    friendship.status = "accepted"
    db.commit()
    
    return {"message": "Solicitud de amistad aceptada"}

@router.get("/my-friends", response_model=List[schemas.FriendshipResponse])
def get_my_friends(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    friendships = db.query(models.Friendship).filter(
        ((models.Friendship.user_id == current_user.id) | (models.Friendship.friend_id == current_user.id)) &
        (models.Friendship.status == "accepted")
    ).all()
    
    result = []
    for friendship in friendships:
        # Determinar quién es el amigo
        if friendship.user_id == current_user.id:
            friend_user = db.query(models.User).filter(models.User.id == friendship.friend_id).first()
        else:
            friend_user = db.query(models.User).filter(models.User.id == friendship.user_id).first()
        
        result.append({
            "id": friendship.id,
            "user_id": friendship.user_id,
            "friend_id": friendship.friend_id,
            "status": friendship.status,
            "friend_email": friend_user.email,
            "friend_name": friend_user.email.split('@')[0]
        })
    
    return result

@router.get("/compare/{friend_id}")
def compare_with_friend(
    friend_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # Verificar que son amigos
    friendship = db.query(models.Friendship).filter(
        ((models.Friendship.user_id == current_user.id) & (models.Friendship.friend_id == friend_id)) |
        ((models.Friendship.user_id == friend_id) & (models.Friendship.friend_id == current_user.id)),
        models.Friendship.status == "accepted"
    ).first()
    
    if not friendship:
        raise HTTPException(status_code=404, detail="No son amigos o la solicitud no está aceptada")
    
    # Obtener datos de ambos usuarios
    my_workouts = db.query(models.Workout).filter(models.Workout.user_id == current_user.id).all()
    friend_workouts = db.query(models.Workout).filter(models.Workout.user_id == friend_id).all()
    
    # Calcular comparativas por ejercicio
    comparison = []
    
    # Ejercicios únicos de ambos usuarios
    my_exercises = set(w.exercise for w in my_workouts)
    friend_exercises = set(w.exercise for w in friend_workouts)
    all_exercises = my_exercises.union(friend_exercises)
    
    for exercise in all_exercises:
        my_max = max([w.weight for w in my_workouts if w.exercise == exercise], default=0)
        friend_max = max([w.weight for w in friend_workouts if w.exercise == exercise], default=0)
        
        comparison.append({
            "exercise": exercise,
            "my_max_weight": my_max,
            "friend_max_weight": friend_max,
            "difference": abs(my_max - friend_max),
            "i_am_stronger": my_max > friend_max
        })
    

    return comparison
