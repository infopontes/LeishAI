from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import Response

from src.db.crud import crud_breed
from src.schemas import breed as breed_schema
from .dependencies import get_current_user, get_db
from .router_roles import (
    get_current_admin_user,
)

router = APIRouter(prefix="/breeds", tags=["Breeds"])


@router.post(
    "/",
    response_model=breed_schema.BreedPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin_user)],
)
def create_new_breed(
    breed: breed_schema.BreedCreate, db: Session = Depends(get_db)
):
    """
    Creates a new race in the system.
    For administrator users only.
    """
    db_breed = crud_breed.get_breed_by_name(db, name=breed.name)
    if db_breed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Breed '{breed.name}' already exists.",
        )
    return crud_breed.create_breed(db=db, breed=breed)


@router.get(
    "/",
    response_model=List[breed_schema.BreedPublic],
    dependencies=[Depends(get_current_user)],
)
def read_breeds(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Returns a list of breeds.
    Accessible to any logged-in user.
    """
    breeds = crud_breed.get_breeds(db, skip=skip, limit=limit)
    return breeds


@router.get(
    "/{breed_id}",
    response_model=breed_schema.BreedPublic,
    dependencies=[Depends(get_current_user)],
)
def read_breed_by_id(breed_id: UUID, db: Session = Depends(get_db)):
    """
    Search for a single breed by its ID.
    """
    db_breed = crud_breed.get_breed_by_id(db, breed_id=breed_id)
    if db_breed is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Breed not found",
        )
    return db_breed


@router.put(
    "/{breed_id}",
    response_model=breed_schema.BreedPublic,
    dependencies=[Depends(get_current_admin_user)],
)
def update_existing_breed(
    breed_id: UUID,
    breed_update: breed_schema.BreedCreate,
    db: Session = Depends(get_db),
):
    """
    Updates the data of an existing race.
    """
    # Checks if the breed with the new name already exists to avoid duplicates
    existing_breed = crud_breed.get_breed_by_name(db, name=breed_update.name)
    if existing_breed and existing_breed.id != breed_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Breed with name '{breed_update.name}' already exists.",
        )

    db_breed = crud_breed.update_breed(
        db=db, breed_id=breed_id, breed_update=breed_update
    )
    if db_breed is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Breed not found",
        )
    return db_breed


@router.delete(
    "/{breed_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin_user)],
)
def delete_existing_breed(
    breed_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Removes an existing race.
    """
    # We added a dependency check: do not allow deleting a breed if there are animals associated with it.
    db_breed = crud_breed.get_breed_by_id(db, breed_id=breed_id)
    if not db_breed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Breed not found",
        )

    if (
        db_breed.animals
    ):  # Checks if the list of animals of the breed is not empty
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete breed with associated animals.",
        )

    crud_breed.delete_breed(db=db, breed_id=breed_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
