from uuid import UUID
from fastapi import Response
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Request,
)
from sqlalchemy.orm import Session
from typing import List

from src.core.limiter import limiter

from src.db.crud import crud_user
from src.schemas import user as user_schema
from src.db import models
from .dependencies import get_current_user, get_db, get_current_admin_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=user_schema.UserPublic,
    status_code=status.HTTP_201_CREATED,
    # Em vez de decorador, usamos o limiter como uma dependência
    dependencies=[Depends(limiter.limit("5/hour"))],
)
def create_new_user(
    request: Request,  # 👈 Adicione o request
    user: user_schema.UserCreate,
    db: Session = Depends(get_db),
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


@router.get(
    "/",
    response_model=List[user_schema.UserPublic],
    dependencies=[Depends(get_current_admin_user)],
)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.put(
    "/{user_id}",
    response_model=user_schema.UserPublic,
    dependencies=[Depends(get_current_admin_user)],  # 👈 Protegido por admin
)
def update_existing_user(
    user_id: UUID,
    user_update: user_schema.UserUpdateAdmin,  # 👈 Usamos o novo schema
    db: Session = Depends(get_db),
):
    """
    Atualiza os dados de um utilizador existente.
    Acessível apenas para administradores.
    """
    db_user = crud_user.update_user(
        db=db, user_id=user_id, user_update=user_update
    )
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return db_user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin_user)],  # 👈 Protegido por admin
)
def deactivate_existing_user(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Desativa ('soft delete') um utilizador existente.
    Acessível apenas para administradores.
    """
    deactivated_user = crud_user.deactivate_user(db=db, user_id=user_id)
    if deactivated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
