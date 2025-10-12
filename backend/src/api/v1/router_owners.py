from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.crud import crud_owner
from src.schemas import owner as owner_schema
from .dependencies import get_current_user, get_db

router = APIRouter(prefix="/owners", tags=["Owners"])


@router.post(
    "/",
    response_model=owner_schema.OwnerPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
def create_new_owner(
    owner: owner_schema.OwnerCreate, db: Session = Depends(get_db)
):
    return crud_owner.create_owner(db=db, owner=owner)


@router.get(
    "/",
    response_model=List[owner_schema.OwnerPublic],
    dependencies=[Depends(get_current_user)],
)
def read_owners(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud_owner.get_owners(db, skip=skip, limit=limit)


@router.get(
    "/{owner_id}",
    response_model=owner_schema.OwnerPublic,
    dependencies=[Depends(get_current_user)],
)
def read_owner_by_id(owner_id: UUID, db: Session = Depends(get_db)):
    db_owner = crud_owner.get_owner_by_id(db, owner_id=owner_id)
    if db_owner is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    return db_owner
