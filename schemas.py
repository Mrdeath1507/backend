from pydantic import BaseModel, field_validator
from datetime import datetime, date
from typing import Optional, List

# ------------------------------
#   USUARIOS
# ------------------------------

class UserBase(BaseModel):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str

    class Config:
        from_attributes = True
# ------------------------------
#   WORKOUTS / ENTRENAMIENTOS
# ------------------------------

class WorkoutBase(BaseModel):
    exercise: str
    weight: float
    reps: int
    sets: int
    muscle_group: str

class WorkoutCreate(WorkoutBase):
    date: Optional[str] = None  # Aceptar como string (YYYY-MM-DD)
    
    @field_validator('date', mode='before')
    @classmethod
    def parse_date(cls, v):
        print(f"[schemas.WorkoutCreate.parse_date] Input value: {v}, type: {type(v)}")
        if isinstance(v, str):
            # Si es solo una fecha (YYYY-MM-DD), convertir a datetime con hora 00:00:00
            try:
                from datetime import datetime as dt
                result = dt.fromisoformat(v + 'T00:00:00')
                print(f"[schemas.WorkoutCreate.parse_date] Parsed successfully: {result}")
                return result
            except Exception as e:
                print(f"[schemas.WorkoutCreate.parse_date] Error parsing: {e}")
                return datetime.fromisoformat(v) if 'T' in v else dt.fromisoformat(v + 'T00:00:00')
        print(f"[schemas.WorkoutCreate.parse_date] Not a string, returning as is: {v}")
        return v

class WorkoutResponse(WorkoutBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True


# ------------------------------
#   PROGRESO
# ------------------------------

class ProgressMetricBase(BaseModel):
    exercise: str
    max_weight: float

class ProgressMetricCreate(ProgressMetricBase):
    pass

class ProgressMetricResponse(ProgressMetricBase):
    id: int
    updated_at: datetime

    class Config:
        from_attributes = True


# ------------------------------
#   TOP 3 RESPONSE
# ------------------------------

class Top3Entry(BaseModel):
    email: str
    exercise: str
    max_weight: float

class Top3Response(BaseModel):
    results: List[Top3Entry]


# ------------------------------
#   AMISTADES
# ------------------------------

class FriendshipBase(BaseModel):
    friend_email: str

class FriendshipCreate(FriendshipBase):
    pass

class FriendshipResponse(BaseModel):
    id: int
    user_id: int
    friend_id: int
    status: str
    friend_email: str
    friend_name: str
    
    class Config:
        from_attributes = True

class FriendComparison(BaseModel):
    exercise: str
    my_max_weight: float
    friend_max_weight: float
    difference: float
    i_am_stronger: bool
