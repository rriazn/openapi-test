import enum
from typing import List
from sqlmodel import Relationship, SQLModel, Field

class ExerciseType(str, enum.Enum):
    WR = "weight and reps"
    RO = "reps"
    CA = "cardio"
    FL = "flexibility"


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str = Field()


class ExerciseWorkoutLink(SQLModel, table=True):
    __tablename__ = "exercise_workout_link"
    workout_id: int = Field(foreign_key="workouts.id", primary_key=True)
    exercise_id: int = Field(foreign_key="exercises.id", primary_key=True)


class Exercise(SQLModel, table=True):
    __tablename__ = "exercises"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    type: ExerciseType = Field()


class Workout(SQLModel, table=True):
    __tablename__ = "workouts"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    user_name: str = Field(foreign_key="users.id")
    exercises: List["Exercise"] = Relationship(link_model=ExerciseWorkoutLink)