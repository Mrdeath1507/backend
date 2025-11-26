from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(
    prefix="/progress",
    tags=["Progress"]
)

@router.post("/")
def add_progress(record: schemas.ProgressMetricCreate, db: Session = Depends(get_db)):
    new_record = models.Progress(**record.dict())
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

@router.get("/{user_id}")
def get_progress(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Progress).filter(models.Progress.user_id == user_id).all()

@router.get("/top3")
def get_top3(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    ranking = []

    for user in users:
        total_weight = 0
        for w in user.workouts:
            total_weight += w.weight_lifted

        ranking.append({
            "username": user.username,
            "total_weight": total_weight
        })

    ranking_sorted = sorted(ranking, key=lambda x: x["total_weight"], reverse=True)

    return ranking_sorted[:3]
