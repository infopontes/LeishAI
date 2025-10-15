from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import Response

from src.db.crud import crud_animal
from src.schemas import animal as animal_schema
from .dependencies import get_current_user, get_db
from typing import List

router = APIRouter(prefix="/animals", tags=["Animals"])


@router.post(
    "/",
    response_model=animal_schema.AnimalPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
def create_new_animal(
    animal: animal_schema.AnimalCreate, db: Session = Depends(get_db)
):
    """
    Creates a new animal in the system, associated with an owner and a breed.
    """
    return crud_animal.create_animal(db=db, animal=animal)


@router.get(
    "/",
    response_model=List[animal_schema.AnimalPublic],
    dependencies=[Depends(get_current_user)],
)
def read_animals(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Returns a list of animals.
    """
    animals = crud_animal.get_animals(db, skip=skip, limit=limit)
    return animals


@router.get(
    "/{animal_id}",
    response_model=animal_schema.AnimalPublic,
    dependencies=[Depends(get_current_user)],
)
def read_animal_by_id(animal_id: UUID, db: Session = Depends(get_db)):
    """
    Search for a single animal by its ID.
    """
    db_animal = crud_animal.get_animal_by_id(db, animal_id=animal_id)
    if db_animal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal not found",
        )
    return db_animal


@router.put(
    "/{animal_id}",
    response_model=animal_schema.AnimalPublic,
    dependencies=[Depends(get_current_user)],
)
def update_existing_animal(
    animal_id: UUID,
    animal_update: animal_schema.AnimalUpdate,
    db: Session = Depends(get_db),
):
    """
    Updates the data of an existing animal.
    """
    db_animal = crud_animal.update_animal(
        db=db, animal_id=animal_id, animal_update=animal_update
    )
    if db_animal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal not found",
        )
    return db_animal


@router.delete(
    "/{animal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
def delete_existing_animal(
    animal_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Removes an existing animal.
    """
    # We added a dependency check: do not allow deleting an animal if there are appointments associated with it.
    db_animal = crud_animal.get_animal_by_id(db, animal_id=animal_id)
    if not db_animal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal not found",
        )

    if db_animal.assessments:  # Check if the animal's care list is not empty
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete animal with associated assessments.",
        )

    crud_animal.delete_animal(db=db, animal_id=animal_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
