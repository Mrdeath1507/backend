from pydantic import BaseModel
from datetime import datetime
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
    pass

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
