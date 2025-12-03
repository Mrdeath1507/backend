from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

    workouts = relationship("Workout", back_populates="user")
    metrics = relationship("ProgressMetric", back_populates="user")


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    exercise = Column(String, index=True)     # Ejemplo: "Press banca"
    weight = Column(Float)                    # Cuánto levantó
    reps = Column(Integer)                    # Repeticiones
    sets = Column(Integer)                    # Series
    muscle_group = Column(String)             # Pecho, espalda, etc.
    date = Column(DateTime, default=datetime.utcnow)

    # Relación inversa
    user = relationship("User", back_populates="workouts")


class ProgressMetric(Base):
    __tablename__ = "progress_metrics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    exercise = Column(String, index=True)     # Ejercicio específico
    max_weight = Column(Float)                # Peso máximo registrado
    updated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="metrics")


class Friendship(Base):
    __tablename__ = "friendships"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    friend_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")  # pending, accepted, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    user = relationship("User", foreign_keys=[user_id], backref="friendships_initiated")
    friend = relationship("User", foreign_keys=[friend_id], backref="friendships_received")
