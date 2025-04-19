from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from uuid import uuid4

from src.db import User, Level
from src.security.password import verify_password, get_password_hash
from src.security.jwt import create_access_token, Token, ACCESS_TOKEN_EXPIRE_MONTHS
from src.schemas.user import UserResponseSchema

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.get_or_none(username=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=60*24*31*ACCESS_TOKEN_EXPIRE_MONTHS)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserResponseSchema)
async def register_user(username: str, password: str, name: str):
    if await User.get_or_none(username=username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    hashed_password = get_password_hash(password)
    user = await User.create(
        id=uuid4(),
        username=username,
        password=hashed_password,
        name=name,
        description="",
        avatar="",
        points=0,
        level=Level.BEGINNER
    )
    
    return UserResponseSchema(
        name=user.name,
        username=user.username,
        description=user.description,
        avatar=user.avatar,
        points=user.points
    )

