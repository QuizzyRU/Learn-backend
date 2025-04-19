from fastapi import APIRouter, HTTPException, Depends
import sqlite3
import os
import shutil
from uuid import uuid4, UUID
from collections import defaultdict
from src.db import Tasks, Solution, Status, Results, Level
from src.schemas.tasks import ExecuteQueryResponseSchema, \
                              VisualizeDatabaseResponseSchema, \
                              GetTaskResponseSchema, \
                              Task, \
                              AllTasksResponseSchema, \
                              SolutionResponseSchema, \
                              SolveResponseSchema, \
                              ResultResponseSchema, \
                              UserTaskStatistics, \
                              UserProgressResponse
from src.schemas.user import UserResponseSchema
from src.security.middleware import JWTBearer

router = APIRouter()
TEMP_DIR = "temp_tasks"

os.makedirs(TEMP_DIR, exist_ok=True)

user_auth = JWTBearer()

@router.get("/all", response_model=AllTasksResponseSchema)
async def get_all_tasks():
    tasks = await Tasks.all()
    result = [Task(id=task.id, level=task.level, db_path=task.db_path, price=task.price, name=task.name, description=task.description) for task in tasks]
    return {"result": result}

@router.get("/user/progress", response_model=UserProgressResponse)
async def get_user_progress(user = Depends(user_auth)):
    completed_results = await Results.filter(
        user=user,
        points_earned__gt=0
    ).prefetch_related('task')
    
    total_points = sum(result.points_earned for result in completed_results)
    
    tasks_by_level = defaultdict(int)
    for result in completed_results:
        tasks_by_level[result.task.level] += 1
    
    recent_results = await Results.filter(
        user=user
    ).limit(10).prefetch_related('task')

    recent_results_schema = [
        ResultResponseSchema(
            id=result.id,
            task=Task(
                id=result.task.id,
                name=result.task.name,
                description=result.task.description,
                level=result.task.level,
                db_path=result.task.db_path,
                price=result.task.price
            ),
            user=UserResponseSchema(
                name=user.name,
                username=user.username,
                description=user.description,
                avatar=user.avatar,
                points=user.points
            ),
            points_earned=result.points_earned
        )
        for result in recent_results
    ]

    statistics = UserTaskStatistics(
        total_tasks_completed=len(completed_results),
        total_points_earned=total_points,
        tasks_by_level=dict(tasks_by_level),
        recent_results=recent_results_schema
    )

    return UserProgressResponse(statistics=statistics)

@router.post("/start/{task_id}", response_model=SolutionResponseSchema)
async def create_solution(task_id: UUID, user = Depends(user_auth)):
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
async def get_solution(task_id: UUID, user = Depends(user_auth)):
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
async def execute_query(task_id: UUID, query: str, user = Depends(user_auth)):
    solution = await Solution.get_or_none(id=task_id)
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")

    temp_file_path = os.path.join(TEMP_DIR, f"{task_id}.sqlite")
    if not os.path.exists(temp_file_path):
        raise HTTPException(status_code=404, detail="Temporary task file not found")

    if solution.status == Status.FINISH:
        raise HTTPException(status_code=403, detail="Solution is finished")

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
async def visualize_database(task_id: UUID, user = Depends(user_auth)):
    solution = await Solution.get_or_none(id=task_id)
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")

    temp_file_path = os.path.join(TEMP_DIR, f"{task_id}.sqlite")
    if not os.path.exists(temp_file_path):
        raise HTTPException(status_code=404, detail="Temporary task file not found")

    if solution.status == Status.FINISH:
        raise HTTPException(status_code=403, detail="Solution is finished")

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
async def solve_task(task_id: UUID, answer: str, user = Depends(user_auth)):
    solution = await Solution.get_or_none(id=task_id).select_related("task")
    if not solution:
        raise HTTPException(status_code=404, detail="Solution not found")
    if solution.status == Status.FINISH:
        raise HTTPException(status_code=403, detail="Solution is finished")

    if solution.task.answer == answer:
        solution.status = Status.FINISH
        await solution.save()
        result = await Results.create(
            id=uuid4(),
            task=solution.task,
            user=user,
            points_earned=solution.task.price
        )

        user.points += solution.task.price
        await user.save()

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
            ),
            result=ResultResponseSchema(
                id=result.id,
                task=Task(
                    id=solution.task.id,
                    level=solution.task.level,
                    db_path=solution.task.db_path,
                    price=solution.task.price,
                    name=solution.task.name,
                    description=solution.task.description
                ),
                user=UserResponseSchema(
                    name=user.name,
                    username=user.username,
                    description=user.description,
                    avatar=user.avatar,
                    points=user.points
                ),
                points_earned=result.points_earned
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
        ),
        result=None
    )