from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, crud, auth, database, models

router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"]
)



@router.post("/add", response_model=schemas.WorkoutResponse)
def add_workout(workout: schemas.WorkoutCreate,
                db: Session = Depends(database.get_db),
                user=Depends(auth.get_current_user)):

    # Guardar el entrenamiento
    workout_db = crud.create_workout(db, workout, user_id=user.id)

    # Actualizar el PR del ejercicio
    crud.update_progress_metric(db, user.id, workout.exercise, workout.weight)

    return workout_db


@router.get("/mine", response_model=list[schemas.WorkoutResponse])
def get_my_workouts(db: Session = Depends(database.get_db),
                    user=Depends(auth.get_current_user)):
    return crud.get_user_workouts(db, user.id)

# Duplicate /mine endpoint removed because 'models' and 'get_db' were not imported.
# The working implementation above uses crud.get_user_workouts and database.get_db.

@router.get("/workouts", response_model=list[schemas.WorkoutResponse])
def get_workouts(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Workout).filter(models.Workout.user_id == current_user.id).all()
