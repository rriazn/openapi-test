from models import Workout
from pydantic import BaseModel, Field
from typing import List

class WorkoutGetListItem(BaseModel):
    id: int = Field(description="ID of the workout")
    name: str = Field(description="Name of the workout")

class WorkoutGetResponse(BaseModel):
    workouts: List[WorkoutGetListItem] = Field(description="List of all workouts with their IDs and names for the user")


class WorkoutDetailResponse(BaseModel):
    name: str = Field(description="Name of the workout")
    owner: str = Field(description="Username of the workout owner")
    exercises: List[str] = Field(description="List of exercise names included in the workout")


class WorkoutCreateRequest(BaseModel):
    workout_name: str = Field(description="Name of the workout", examples=["Morning Routine", "Leg Day"])
    exercise_ids: List[int] = Field(description="List of exercise IDs to include in the workout")


class WorkoutCreateResponse(BaseModel):
    name: str = Field(description="Name of the created workout")
    owner: str = Field(description="Username of the workout owner")
    exercises: List[str] = Field(description="List of exercise names included in the workout")
