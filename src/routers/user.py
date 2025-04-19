from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from src.security.middleware import JWTBearer
from src.schemas.user import UserResponseSchema, UserUpdateSchema
from src.db.models.user import User
import os
import shutil
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