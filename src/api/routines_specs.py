from models import Routine
from pydantic import BaseModel, Field
from typing import List

class RoutineGetListItem(BaseModel):
    id: int = Field(description="ID of the routine")
    name: str = Field(description="Name of the routine")

class RoutineGetResponse(BaseModel):
    routines: List[RoutineGetListItem] = Field(description="List of all routines with their IDs and names for the user")


class RoutineDetailResponse(BaseModel):
    name: str = Field(description="Name of the routine")
    owner: str = Field(description="Username of the routine owner")
    exercises: List[str] = Field(description="List of exercise names included in the routine")


class RoutineCreateRequest(BaseModel):
    routine_name: str = Field(description="Name of the routine", examples=["Morning Routine", "Leg Day"])
    exercise_ids: List[int] = Field(description="List of exercise IDs to include in the routine")


class RoutineCreateResponse(BaseModel):
    id: int = Field(description="ID of the created routine")
    name: str = Field(description="Name of the created routine")
    owner: str = Field(description="Username of the routine owner")
    exercises: List[str] = Field(description="List of exercise names included in the routine")


class ActionResponse(BaseModel):
    message: str = Field(description="Message describing the result of the action")
