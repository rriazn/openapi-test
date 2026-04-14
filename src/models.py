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


class ExerciseRoutineLink(SQLModel, table=True):
    __tablename__ = "exercise_routine_link"
    routine_id: int = Field(foreign_key="routines.id", primary_key=True)
    exercise_id: int = Field(foreign_key="exercises.id", primary_key=True)


class Exercise(SQLModel, table=True):
    __tablename__ = "exercises"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    type: ExerciseType = Field()


class Routine(SQLModel, table=True):
    __tablename__ = "routines"
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    user_name: str = Field(foreign_key="users.id")
    exercises: List["Exercise"] = Relationship(link_model=ExerciseRoutineLink)