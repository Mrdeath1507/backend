from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import traceback

import schemas, crud, auth, database, models

router = APIRouter(
    prefix="/workouts",
    tags=["Workouts"]
)



@router.post("/add", response_model=schemas.WorkoutResponse)
def add_workout(workout: schemas.WorkoutCreate,
                db: Session = Depends(database.get_db),
                user=Depends(auth.get_current_user)):
    try:
        # Logging para debug
        print(f"[workouts.add_workout] user_id={getattr(user, 'id', None)}")
        print(f"[workouts.add_workout] workout object: {workout}")
        print(f"[workouts.add_workout] workout.exercise={workout.exercise}, workout.date={workout.date}, type(workout.date)={type(workout.date)}")

        # Guardar el entrenamiento
        workout_db = crud.create_workout(db, workout, user_id=user.id)

        # Actualizar el PR del ejercicio
        crud.update_progress_metric(db, user.id, workout.exercise, workout.weight)

        print(f"[workouts.add_workout] Saved workout id={workout_db.id}")
        return workout_db
    except Exception as e:
        # Imprimir stacktrace en logs para identificar el problema
        print("[workouts.add_workout] Exception:")
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/mine", response_model=list[schemas.WorkoutResponse])
def get_my_workouts(db: Session = Depends(database.get_db),
                    user=Depends(auth.get_current_user)):
    return crud.get_user_workouts(db, user.id)

# Duplicate /mine endpoint removed because 'models' and 'get_db' were not imported.
# The working implementation above uses crud.get_user_workouts and database.get_db.

@router.get("/workouts", response_model=list[schemas.WorkoutResponse])
def get_workouts(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return db.query(models.Workout).filter(models.Workout.user_id == current_user.id).all()
