<<<<<<< HEAD
from sqlalchemy.orm import Session
from . import models, schemas
from .auth import hash_password


# ----------------------
#   USERS
# ----------------------

def create_user(db: Session, user: schemas.UserCreate):
    # Verificar que el nombre de usuario no exista
    if db.query(models.User).filter(models.User.username == user.username).first():
        raise ValueError("El nombre de usuario ya está en uso")
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise ValueError("El email ya está en uso")
    user_db = models.User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password)
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


# ----------------------
#   WORKOUTS
# ----------------------

def create_workout(db: Session, workout: schemas.WorkoutCreate, user_id: int):
    workout_db = models.Workout(
        user_id=user_id,
        exercise=workout.exercise,
        weight=workout.weight,
        reps=workout.reps,
        sets=workout.sets,
        muscle_group=workout.muscle_group
    )

    db.add(workout_db)
    db.commit()
    db.refresh(workout_db)
    return workout_db


def get_user_workouts(db: Session, user_id: int):
    return db.query(models.Workout).filter(
        models.Workout.user_id == user_id
    ).order_by(models.Workout.date.desc()).all()


# ----------------------
#   PROGRESS METRICS
# ----------------------

def update_progress_metric(db: Session, user_id: int, exercise: str, weight: float):
    metric = db.query(models.ProgressMetric).filter(
        models.ProgressMetric.user_id == user_id,
        models.ProgressMetric.exercise == exercise
    ).first()

    if metric:
        if weight > metric.max_weight:
            metric.max_weight = weight
            db.commit()
            db.refresh(metric)
        return metric

    # Si no existe, crearla
    new_metric = models.ProgressMetric(
        user_id=user_id,
        exercise=exercise,
        max_weight=weight
    )
    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)
    return new_metric


def get_top3(db: Session, exercise: str):
    return db.query(models.User.username,
                    models.ProgressMetric.exercise,
                    models.ProgressMetric.max_weight).join(
        models.ProgressMetric,
        models.User.id == models.ProgressMetric.user_id
    ).filter(models.ProgressMetric.exercise == exercise).order_by(
        models.ProgressMetric.max_weight.desc()
    ).limit(3).all()
=======
from sqlalchemy.orm import Session
import models, schemas
from auth import hash_password


# ----------------------
#   USERS
# ----------------------

def create_user(db: Session, user: schemas.UserCreate):
    user_db = models.User(
        username=user.username,
        password_hash=hash_password(user.password)
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


# ----------------------
#   WORKOUTS
# ----------------------

def create_workout(db: Session, workout: schemas.WorkoutCreate, user_id: int):
    workout_db = models.Workout(
        user_id=user_id,
        exercise=workout.exercise,
        weight=workout.weight,
        reps=workout.reps,
        sets=workout.sets,
        muscle_group=workout.muscle_group
    )

    db.add(workout_db)
    db.commit()
    db.refresh(workout_db)
    return workout_db


def get_user_workouts(db: Session, user_id: int):
    return db.query(models.Workout).filter(
        models.Workout.user_id == user_id
    ).order_by(models.Workout.date.desc()).all()


# ----------------------
#   PROGRESS METRICS
# ----------------------

def update_progress_metric(db: Session, user_id: int, exercise: str, weight: float):
    metric = db.query(models.ProgressMetric).filter(
        models.ProgressMetric.user_id == user_id,
        models.ProgressMetric.exercise == exercise
    ).first()

    if metric:
        if weight > metric.max_weight:
            metric.max_weight = weight
            db.commit()
            db.refresh(metric)
        return metric

    # Si no existe, crearla
    new_metric = models.ProgressMetric(
        user_id=user_id,
        exercise=exercise,
        max_weight=weight
    )
    db.add(new_metric)
    db.commit()
    db.refresh(new_metric)
    return new_metric


def get_top3(db: Session, exercise: str):
    return db.query(models.User.username,
                    models.ProgressMetric.exercise,
                    models.ProgressMetric.max_weight).join(
        models.ProgressMetric,
        models.User.id == models.ProgressMetric.user_id
    ).filter(models.ProgressMetric.exercise == exercise).order_by(
        models.ProgressMetric.max_weight.desc()
    ).limit(3).all()

>>>>>>> 706d10440f265cf7ae62f1ffaba147ebb1bd4b16
