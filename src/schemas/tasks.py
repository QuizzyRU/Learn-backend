from pydantic import BaseModel
from typing import List, Dict, Any

class UploadTaskSchema(BaseModel):
    level: str
    answer: str
    price: int

class UploadTaskResponseSchema(BaseModel):
    task_id: str
    message: str

class ExecuteQueryResponseSchema(BaseModel):
    result: List[Any]

class VisualizeDatabaseResponseSchema(BaseModel):
    structure: Dict[str, List[Any]]

class GetTaskResponseSchema(BaseModel):
    temp_file_path: str