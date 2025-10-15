from typing import List
from sqlalchemy.orm import Session
from src.db import models
from src.schemas import breed as breed_schema
from uuid import UUID


def get_breed_by_name(db: Session, name: str) -> models.Breed | None:
    """
    Search for a breed by name. The search is case-insensitive.
    """
    return db.query(models.Breed).filter(models.Breed.name.ilike(name)).first()


def create_breed(db: Session, breed: breed_schema.BreedCreate) -> models.Breed:
    """
    Creates a new race in the database.
    """
    db_breed = models.Breed(name=breed.name)
    db.add(db_breed)
    db.commit()
    db.refresh(db_breed)
    return db_breed


def get_breeds(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.Breed]:
    """
    Search for a list of breeds with pagination.
    """
    return db.query(models.Breed).offset(skip).limit(limit).all()


def get_breed_by_id(db: Session, breed_id: UUID) -> models.Breed | None:
    """
    Search for a breed by its ID.
    """
    return db.query(models.Breed).filter(models.Breed.id == breed_id).first()


def update_breed(
    db: Session, breed_id: UUID, breed_update: breed_schema.BreedCreate
) -> models.Breed | None:
    """
    Updates the data of an existing race.
    """
    db_breed = get_breed_by_id(db, breed_id=breed_id)
    if not db_breed:
        return None

    # Gets the update schema data as a dictionary
    update_data = breed_update.model_dump(exclude_unset=True)

    # Iterates over the data and updates the fields of the SQLAlchemy object
    for key, value in update_data.items():
        setattr(db_breed, key, value)

    db.add(db_breed)
    db.commit()
    db.refresh(db_breed)
    return db_breed


def delete_breed(db: Session, breed_id: UUID) -> models.Breed | None:
    """
    Removes a breed from the database by its ID.
    """
    db_breed = get_breed_by_id(db, breed_id=breed_id)
    if not db_breed:
        return None

    # We added a check to not delete the "SRD (No Defined Breed)" breed
    if db_breed.name == "SRD (Sem Raça Definida)":
        return None  # Or raise an exception, depending on the business rule

    db.delete(db_breed)
    db.commit()
    return db_breed
