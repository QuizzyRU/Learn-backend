from fastapi import APIRouter, HTTPException
import sqlite3
import os
import shutil
from uuid import uuid4, UUID
from src.db import Tasks, Solution, Status
from src.schemas.tasks import ExecuteQueryResponseSchema, \
                              VisualizeDatabaseResponseSchema, \
                              GetTaskResponseSchema, \
                              Task, \
                              AllTasksResponseSchema, \
                              SolutionResponseSchema, \
                              SolveResponseSchema

router = APIRouter()
TEMP_DIR = "temp_tasks"

os.makedirs(TEMP_DIR, exist_ok=True)

@router.get("/all", response_model=AllTasksResponseSchema)
async def get_all_tasks():
    tasks = await Tasks.all()
    result = [Task(id=task.id, level=task.level, db_path=task.db_path, price=task.price, name=task.name, description=task.description) for task in tasks]
    return {"result": result}

@router.post("/start/{task_id}", response_model=SolutionResponseSchema)
async def create_solution(task_id: UUID):
    task = await Tasks.get_or_none(id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    id = uuid4()
    solution = await Solution.create(
        id=id,
        task=task,
        status=Status.START
    )

    temp_file_path = os.path.join(TEMP_DIR, f"{id}.sqlite")
    shutil.copy(task.db_path, temp_file_path)

    return SolutionResponseSchema(
        id=solution.id,
        task=Task(
            id=task.id,
            level=task.level,
            db_path=task.db_path,
            price=task.price,
            name=task.name,
            description=task.description
        ),
        status=solution.status
    )

@router.get("/{task_id}", response_model=SolutionResponseSchema)
async def get_solution(task_id: UUID):
    solution = await Solution.get_or_none(id=task_id).select_related("task")
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")
    return SolutionResponseSchema(
        id=solution.id,
        task=Task(
            id=solution.task.id,
            level=solution.task.level,
            db_path=solution.task.db_path,
            price=solution.task.price,
            name=solution.task.name,
            description=solution.task.description
        ),
        status=solution.status
    )

@router.post("/{task_id}/execute", response_model=ExecuteQueryResponseSchema)
async def execute_query(task_id: UUID, query: str):
    solution = await Solution.get_or_none(id=task_id)
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")

    temp_file_path = os.path.join(TEMP_DIR, f"{task_id}.sqlite")
    if not os.path.exists(temp_file_path):
        raise HTTPException(status_code=404, detail="Temporary task file not found")

    if solution.status == Status.FINISH:
        return HTTPException(status_code=403, detail="Solution is finished")

    solution.status = Status.SOLVE
    await solution.save()

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
async def visualize_database(task_id: UUID):
    solution = await Solution.get_or_none(id=task_id)
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")

    temp_file_path = os.path.join(TEMP_DIR, f"{task_id}.sqlite")
    if not os.path.exists(temp_file_path):
        raise HTTPException(status_code=404, detail="Temporary task file not found")

    if solution.status == Status.FINISH:
        return HTTPException(status_code=403, detail="Solution is finished")

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
                structure[table_name] = {
                    "columns": [
                        {"name": col[1], "type": col[2], "notnull": col[3], "default": col[4], "pk": col[5]} for col in columns
                    ]
                }

                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
                rows = cursor.fetchall()
                structure[table_name]["sample_data"] = rows
    except sqlite3.Error as e:
        raise HTTPException(status_code=400, detail=f"SQL Error: {e}")

    return {"structure": structure}

@router.post("/solve/{task_id}", response_model=SolveResponseSchema)
async def solve_task(task_id: UUID, answer: str):
    solution = await Solution.get_or_none(id=task_id).select_related("task")
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")
    if solution.status == Status.FINISH:
        return HTTPException(status_code=403, detail="Solution is finished")
    if solution.task.answer == answer:
        solution.status = Status.FINISH
        await solution.save()
        return SolveResponseSchema(
            message="You have entered the correct answer!",
            solution=SolutionResponseSchema(
                id=solution.id,
                task=Task(
                    id=solution.task.id,
                    level=solution.task.level,
                    db_path=solution.task.db_path,
                    price=solution.task.price,
                    name=solution.task.name,
                    description=solution.task.description
                ),
                status=solution.status
            )
        )


    return SolveResponseSchema(
        message="You entered the wrong answer.",
        solution=SolutionResponseSchema(
            id=solution.id,
            task=Task(
                id=solution.task.id,
                level=solution.task.level,
                db_path=solution.task.db_path,
                price=solution.task.price,
                name=solution.task.name,
                description=solution.task.description
            ),
            status=solution.status
        )
    )