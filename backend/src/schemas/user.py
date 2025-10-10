from uuid import UUID
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from .role import RolePublic


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: UUID
    is_active: bool
    role: Optional[RolePublic] = None
    model_config = ConfigDict(from_attributes=True)
