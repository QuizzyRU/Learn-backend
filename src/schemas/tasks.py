from uuid import UUID
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime
from src.db import Level, Status
from .user import UserResponseSchema

class UploadTaskSchema(BaseModel):
    name: str
    description: str
    level: Level
    answer: str
    price: int

class UploadTaskResponseSchema(BaseModel):
    task_id: str
    message: str

class Task(BaseModel):
    id: UUID
    name: str
    description: str
    level: Level
    db_path: str
    price: int

class ExecuteQueryResponseSchema(BaseModel):
    result: List[Any]

class VisualizeDatabaseResponseSchema(BaseModel):
    structure: Dict[str, Dict[str, Any]]

class GetTaskResponseSchema(BaseModel):
    temp_file_path: str

class AllTasksResponseSchema(BaseModel):
    result: List[Task]

class SolutionResponseSchema(BaseModel):
    id: UUID
    task: Task
    status: Status

class ResultResponseSchema(BaseModel):
    id: UUID
    task: Task
    user: UserResponseSchema
    points_earned: int

class SolveResponseSchema(BaseModel):
    message: str
    solution: SolutionResponseSchema
    result: ResultResponseSchema | None = None

class UserTaskStatistics(BaseModel):
    total_tasks_completed: int
    total_points_earned: int
    tasks_by_level: Dict[Level, int]
    recent_results: List[ResultResponseSchema]

class UserProgressResponse(BaseModel):
    statistics: UserTaskStatistics