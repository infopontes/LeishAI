from typing import List
from sqlalchemy.orm import Session
from src.db import models
from src.schemas import breed as breed_schema


def get_breed_by_name(db: Session, name: str) -> models.Breed | None:
    """
    Busca uma raça pelo nome. A busca é 'case-insensitive'.
    """
    return db.query(models.Breed).filter(models.Breed.name.ilike(name)).first()


def create_breed(db: Session, breed: breed_schema.BreedCreate) -> models.Breed:
    """
    Cria uma nova raça no banco de dados.
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
    Busca uma lista de raças com paginação.
    """
    return db.query(models.Breed).offset(skip).limit(limit).all()
