from uuid import UUID
from pydantic import BaseModel
from typing import List, Dict, Any
from src.db import Level, Status

class UploadTaskSchema(BaseModel):
    level: str
    answer: str
    price: int

class UploadTaskResponseSchema(BaseModel):
    task_id: str
    message: str

class Task(BaseModel):
    id: UUID
    level: Level
    db_path: str
    price: int

class ExecuteQueryResponseSchema(BaseModel):
    result: List[Any]

class VisualizeDatabaseResponseSchema(BaseModel):
    structure: Dict[str, List[Any]]

class GetTaskResponseSchema(BaseModel):
    temp_file_path: str

class AllTasksResponseSchema(BaseModel):
    result: List[Task]

class SolutionResponseSchema(BaseModel):
    id: UUID
    task: Task
    status: Status