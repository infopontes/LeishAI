from sqlalchemy.orm import Session
from src.db import models
from src.schemas import animal as animal_schema
from typing import List
from uuid import UUID


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


def get_animal_by_original_id(
    db: Session, original_id: str
) -> models.Animal | None:
    """
    Busca um animal pelo seu ID do banco de dados original.
    """
    return (
        db.query(models.Animal)
        .filter(models.Animal.original_id == original_id)
        .first()
    )


def get_animal_by_id(db: Session, animal_id: UUID) -> models.Animal | None:
    """
    Busca um animal pelo seu ID.
    """
    return (
        db.query(models.Animal).filter(models.Animal.id == animal_id).first()
    )


def update_animal(
    db: Session, animal_id: UUID, animal_update: animal_schema.AnimalUpdate
) -> models.Animal | None:
    """
    Atualiza os dados de um animal existente.
    """
    db_animal = get_animal_by_id(db, animal_id=animal_id)
    if not db_animal:
        return None

    # Obtém os dados do schema de atualização como um dicionário
    update_data = animal_update.model_dump(exclude_unset=True)

    # Itera sobre os dados e atualiza os campos do objeto SQLAlchemy
    for key, value in update_data.items():
        setattr(db_animal, key, value)

    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal


def delete_animal(db: Session, animal_id: UUID) -> models.Animal | None:
    """
    Remove um animal do banco de dados pelo seu ID.
    """
    db_animal = get_animal_by_id(db, animal_id=animal_id)
    if not db_animal:
        return None

    db.delete(db_animal)
    db.commit()
    return db_animal
