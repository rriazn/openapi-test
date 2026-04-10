
from pydantic import BaseModel, Field
from typing import List
from models import Exercise


class ExercisesGetResponse(BaseModel):
    exercises: List[Exercise] = Field(description="List of all exercises")