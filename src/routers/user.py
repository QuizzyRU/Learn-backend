from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from src.security.middleware import JWTBearer
from src.schemas.user import UserResponseSchema, UserUpdateSchema, UsersResponseSchema
from src.schemas.tasks import Task, \
                              ResultResponseSchema, \
                              UserTaskStatistics, \
                              UserProgressResponse
from src.db import User, Results
import os
import shutil
from collections import defaultdict
from uuid import uuid4

router = APIRouter()
user_auth = JWTBearer()

AVATAR_DIR = "avatars"
os.makedirs(AVATAR_DIR, exist_ok=True)

@router.get("/me", response_model=UserResponseSchema)
async def get_current_user(user = Depends(user_auth)):
    return UserResponseSchema(
        name=user.name,
        username=user.username,
        description=user.description,
        avatar=user.avatar,
        points=user.points
    )


@router.get("/progress/{username}", response_model=UserProgressResponse)
async def get_user_progress(username):
    user = await User.get_or_none(username=username)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

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

@router.get("/all", response_model=UsersResponseSchema)
async def get_all_users():
    return UsersResponseSchema(
        users=[UserResponseSchema(
                name=user.name,
                username=user.username,
                description=user.description,
                avatar=user.avatar,
                points=user.points
    ) for user in await User.all()])

@router.get("/top", response_model=UsersResponseSchema)
async def top_users():
    return UsersResponseSchema(
        users=[UserResponseSchema(
                name=user.name,
                username=user.username,
                description=user.description,
                avatar=user.avatar,
                points=user.points
    ) for user in await User.all().order_by("-points").limit(100)])

@router.get("/{username}", response_model=UserResponseSchema)
async def get_user_by_username(username: str):
    user = await User.get_or_none(username=username)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return UserResponseSchema(
        name=user.name,
        username=user.username,
        description=user.description,
        avatar=user.avatar,
        points=user.points
    )
    

@router.patch("/profile", response_model=UserResponseSchema)
async def update_profile(
    update_data: UserUpdateSchema,
    user = Depends(user_auth)
):
    if update_data.username and update_data.username != user.username:
        existing_user = await User.get_or_none(username=update_data.username)
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Username already taken"
            )
    
    if update_data.name is not None:
        user.name = update_data.name
    if update_data.username is not None:
        user.username = update_data.username
    if update_data.description is not None:
        user.description = update_data.description
    
    await user.save()
    
    return UserResponseSchema(
        name=user.name,
        username=user.username,
        description=user.description,
        avatar=user.avatar,
        points=user.points
    )

@router.post("/avatar", response_model=UserResponseSchema)
async def upload_avatar(
    file: UploadFile = File(...),
    user = Depends(user_auth)
):
    if not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail="File must be an image"
        )
    
    
    file_ext = os.path.splitext(file.filename)[1]
    avatar_name = f"{uuid4()}{file_ext}"
    avatar_path = os.path.join(AVATAR_DIR, avatar_name)
    
    with open(avatar_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    old_avatar = user.avatar
    user.avatar = avatar_path
    await user.save()
    
    if old_avatar and os.path.exists(old_avatar):
        try:
            os.remove(old_avatar)
        except:
            pass 
    
    return UserResponseSchema(
        name=user.name,
        username=user.username,
        description=user.description,
        avatar=user.avatar,
        points=user.points
    )