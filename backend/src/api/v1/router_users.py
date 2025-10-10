from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.crud import crud_user
from src.schemas import user as user_schema
from src.db import models
from .dependencies import get_current_user, get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=user_schema.UserPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_new_user(
    user: user_schema.UserCreate, db: Session = Depends(get_db)
):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return crud_user.create_user(db=db, user=user)


@router.get("/me", response_model=user_schema.UserPublic)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user
