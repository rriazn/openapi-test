from pydantic import BaseModel, Field
from typing import List

from models import Exercise, Workout


class WorkoutStartResponse(BaseModel):
    workout: Workout = Field(description="Details of the started workout, including exercises and their types")


class WorkoutEditRequest(BaseModel):
    exercise_add: List[int] = Field(description="List of exercise IDs to add to the workout")
    exercise_remove: List[int] = Field(description="List of exercise IDs to remove from the workout")


class WorkoutEditResponse(BaseModel):
    exercises: List[Exercise] = Field(description="Updated list of exercises included in the workout")
