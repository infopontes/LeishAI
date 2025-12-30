from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Request,
    Response,
)
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from src.core.limiter import limiter
from src.db.crud import crud_user
from src.schemas import user as user_schema
from src.db import models
from .dependencies import get_current_user, get_db, get_current_admin_user
from src.core.config import settings
from src.core import security
from src.services.email import send_user_activation_email

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=user_schema.UserPublic,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/hour")
def create_new_user(
    request: Request,
    user: user_schema.UserCreate,
    db: Session = Depends(get_db),
):
    """Creates a new user in the system."""
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    created_user = crud_user.create_user(db=db, user=user)

    admin_email = (
        settings.ADMIN_NOTIFICATION_EMAIL
        or settings.DEFAULT_ADMIN_EMAIL
        or settings.EMAIL_FROM
    )
    token = security.create_activation_token(str(created_user.id))
    activation_url = (
        f"{settings.BACKEND_BASE_URL}/users/activate?token={token}"
    )
    send_user_activation_email(
        admin_email=admin_email,
        activation_url=activation_url,
        user_email=created_user.email,
        full_name=created_user.full_name,
        reason=user.reason,
    )

    return created_user


@router.get("/me", response_model=user_schema.UserPublic)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    """Returns the data of the currently logged in user."""
    return current_user


@router.get(
    "/",
    response_model=List[user_schema.UserPublic],
    dependencies=[Depends(get_current_admin_user)],
)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Returns a list of all users (admins only)."""
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.put(
    "/{user_id}",
    response_model=user_schema.UserPublic,
    dependencies=[Depends(get_current_admin_user)],
)
def update_existing_user(
    user_id: UUID,
    user_update: user_schema.UserUpdateAdmin,
    db: Session = Depends(get_db),
):
    """Updates an existing user (admins only)."""
    db_user = crud_user.update_user(
        db=db, user_id=user_id, user_update=user_update
    )
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin_user)],
)
def deactivate_existing_user(user_id: UUID, db: Session = Depends(get_db)):
    """Deactivates ('soft delete') a user (admins only)."""
    deactivated_user = crud_user.deactivate_user(db=db, user_id=user_id)
    if deactivated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/activate")
@limiter.limit("20/minute")
def activate_user(
    request: Request, token: str, db: Session = Depends(get_db)
):
    """
    Activates a user using a signed activation token.
    """
    user_id = security.verify_activation_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired activation token",
        )

    db_user = crud_user.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db_user.is_active = True
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"detail": "User activated successfully"}
