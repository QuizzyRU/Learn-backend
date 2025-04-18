from fastapi import APIRouter, UploadFile, HTTPException, Depends
from uuid import uuid4
import os
from src.db.models.tasks import Tasks
from src.schemas.tasks import UploadTaskSchema, UploadTaskResponseSchema

router = APIRouter()

TASKS_DIR = "tasks"

@router.post("/upload-task/", response_model=UploadTaskResponseSchema)
async def upload_task(
    file: UploadFile, 
    task_data: UploadTaskSchema = Depends()
):
    os.makedirs(TASKS_DIR, exist_ok=True)

    task_id = str(uuid4())

    file_path = os.path.join(TASKS_DIR, f"{task_id}.sqlite")

    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        task = await Tasks.create(
            id=task_id,
            level=task_data.level,
            db_path=file_path,
            answer=task_data.answer,
            price=task_data.price
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error saving task: {e}")

    return UploadTaskResponseSchema(task_id=task_id, message="Task uploaded successfully")