from fastapi import APIRouter, HTTPException
import sqlite3
import os
import shutil
from uuid import uuid4
from src.db.models.tasks import Tasks
from src.schemas.tasks import ExecuteQueryResponseSchema, VisualizeDatabaseResponseSchema, GetTaskResponseSchema

router = APIRouter()
TEMP_DIR = "temp_tasks"

os.makedirs(TEMP_DIR, exist_ok=True)

@router.get("/{task_id}", response_model=GetTaskResponseSchema)
async def get_task(task_id: str):
    task = await Tasks.get_or_none(id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    temp_file_path = os.path.join(TEMP_DIR, f"{uuid4()}.sqlite")
    shutil.copy(task.db_path, temp_file_path)

    return {"temp_file_path": temp_file_path}

@router.post("/{task_id}/execute", response_model=ExecuteQueryResponseSchema)
async def execute_query(task_id: str, query: str):
    temp_file_path = os.path.join(TEMP_DIR, f"{task_id}.sqlite")
    if not os.path.exists(temp_file_path):
        raise HTTPException(status_code=404, detail="Temporary task file not found")

    try:
        with sqlite3.connect(temp_file_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            conn.commit()
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=f"SQL Error: {e}")

    return {"result": result}

@router.get("/{task_id}/visualize", response_model=VisualizeDatabaseResponseSchema)
async def visualize_database(task_id: str):
    temp_file_path = os.path.join(TEMP_DIR, f"{task_id}.sqlite")
    if not os.path.exists(temp_file_path):
        raise HTTPException(status_code=404, detail="Temporary task file not found")

    try:
        with sqlite3.connect(temp_file_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()

            structure = {}
            for table in tables:
                table_name = table[0]
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                structure[table_name] = columns
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=f"SQL Error: {e}")

    return {"structure": structure}