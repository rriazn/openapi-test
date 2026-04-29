from models import Exercise, Routine
from pydantic import BaseModel, Field
from typing import List

class ExerciseBase(BaseModel):
    model_config = {"from_attributes": True}
    name: str = Field(description="Name of the exercise", example="Push-up")
    type: str = Field(description="Type of the exercise", example="weight and reps")
    id: int = Field(description="ID of the exercise", example=1)


class RoutineGetListItem(BaseModel):
    id: int = Field(description="ID of the routine")
    name: str = Field(description="Name of the routine")


class RoutineGetResponse(BaseModel):
    routines: List[RoutineGetListItem] = Field(description="List of all routines with their IDs and names for the user")


class RoutineDetailResponse(BaseModel):
    name: str = Field(description="Name of the routine")
    owner: str = Field(description="Username of the routine owner")
    exercises: List[ExerciseBase] = Field(description="List of exercises included in the routine")


class RoutineCreateRequest(BaseModel):
    routine_name: str = Field(description="Name of the routine", examples=["Morning Routine", "Leg Day"])
    exercise_ids: List[int] = Field(description="List of exercise IDs to include in the routine")


class RoutineCreateDetail(BaseModel):
    id: int = Field(description="ID of the created routine")
    name: str = Field(description="Name of the created routine")
    user_name: str = Field(description="Username of the routine owner")
    exercises: List[ExerciseBase] = Field(description="List of exercises included in the created routine")


class RoutineCreateResponse(BaseModel):
    routine: RoutineCreateDetail = Field(description="Details of the created routine, including its ID, name, owner, and exercises")


class RoutineEditRequest(BaseModel):
    routine_name: str = Field(description="New name of the routine", examples=["Updated Routine Name"])
    exercise_add: List[int] = Field(description="List of exercise IDs to add to the routine")
    exercise_remove: List[int] = Field(description="List of exercise IDs to remove from the routine")


class RoutineEditResponse(BaseModel):
    name: str = Field(description="Name of the edited routine")
    exercises: List[ExerciseBase] = Field(description="Updated list of exercises included in the routine")


class ActionResponse(BaseModel):
    message: str = Field(description="Message describing the result of the action")
