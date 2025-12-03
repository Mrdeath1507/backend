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
    date: Optional[datetime] = None  # Aceptar como datetime o string
    
    @field_validator('date', mode='before')
    @classmethod
    def parse_date(cls, v):
        """Convertir date a datetime si es necesario"""
        from datetime import datetime as dt
        
        # Si es None o está vacío, usar la fecha actual
        if v is None or (isinstance(v, str) and v.strip() == ''):
            return dt.utcnow()
        
        # Si ya es datetime, retornar
        if isinstance(v, datetime):
            return v
        
        # Si es string, parsear
        if isinstance(v, str):
            try:
                v = v.strip()
                # Si es formato YYYY-MM-DD, agregar hora
                if len(v) == 10 and v.count('-') == 2:
                    v = v + 'T00:00:00'
                return dt.fromisoformat(v)
            except Exception as e:
                print(f"[schemas] Error parsing date '{v}': {e}")
                return dt.utcnow()
        
        return dt.utcnow()

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
