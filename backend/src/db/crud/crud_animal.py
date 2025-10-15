from sqlalchemy.orm import Session
from src.db import models
from src.schemas import animal as animal_schema
from typing import List
from uuid import UUID


def create_animal(
    db: Session, animal: animal_schema.AnimalCreate
) -> models.Animal:
    """
    Creates a new animal in the database.
    """
    # We use model_dump() to create the data dictionary from the schema
    # and the ** to unpack it as arguments to the SQLAlchemy template.
    db_animal = models.Animal(**animal.model_dump())
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal


def get_animals(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.Animal]:
    """
    Search for a list of animals with pagination.
    """
    return db.query(models.Animal).offset(skip).limit(limit).all()


def get_animal_by_original_id(
    db: Session, original_id: str
) -> models.Animal | None:
    """
    Search for an animal by its ID from the original database.
    """
    return (
        db.query(models.Animal)
        .filter(models.Animal.original_id == original_id)
        .first()
    )


def get_animal_by_id(db: Session, animal_id: UUID) -> models.Animal | None:
    """
    Search for an animal by its ID.
    """
    return (
        db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    )


def update_animal(
    db: Session, animal_id: UUID, animal_update: animal_schema.AnimalUpdate
) -> models.Animal | None:
    """
    Updates the data of an existing animal.
    """
    db_animal = get_animal_by_id(db, animal_id=animal_id)
    if not db_animal:
        return None

    # Gets the update schema data as a dictionary
    update_data = animal_update.model_dump(exclude_unset=True)

    # Iterates over the data and updates the fields of the SQLAlchemy object
    for key, value in update_data.items():
        setattr(db_animal, key, value)

    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal


def delete_animal(db: Session, animal_id: UUID) -> models.Animal | None:
    """
    Removes an animal from the database by its ID.
    """
    db_animal = get_animal_by_id(db, animal_id=animal_id)
    if not db_animal:
        return None

    db.delete(db_animal)
    db.commit()
    return db_animal
