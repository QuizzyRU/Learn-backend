from pydantic import BaseModel
from typing import Optional

class UserResponseSchema(BaseModel):
    name: str
    username: str
    description: str
    avatar: str
    points: int

class UsersResponseSchema(BaseModel):
    users: list[UserResponseSchema]

class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    description: Optional[str] = None