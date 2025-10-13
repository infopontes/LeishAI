from sqlalchemy.orm import Session
from src.db import models
from src.schemas import animal as animal_schema
from typing import List


def create_animal(
    db: Session, animal: animal_schema.AnimalCreate
) -> models.Animal:
    """
    Cria um novo animal no banco de dados.
    """
    # Usamos o model_dump() para criar o dicionário de dados a partir do schema
    # e o ** para desempacotá-lo como argumentos para o modelo SQLAlchemy.
    db_animal = models.Animal(**animal.model_dump())
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal


def get_animals(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.Animal]:
    """
    Busca uma lista de animais com paginação.
    """
    return db.query(models.Animal).offset(skip).limit(limit).all()
