from typing import List
from sqlalchemy.orm import Session
from src.db import models
from src.schemas import breed as breed_schema
from uuid import UUID


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


def get_breed_by_id(db: Session, breed_id: UUID) -> models.Breed | None:
    """
    Busca uma raça pelo seu ID.
    """
    return db.query(models.Breed).filter(models.Breed.id == breed_id).first()


def update_breed(
    db: Session, breed_id: UUID, breed_update: breed_schema.BreedCreate
) -> models.Breed | None:
    """
    Atualiza os dados de uma raça existente.
    """
    db_breed = get_breed_by_id(db, breed_id=breed_id)
    if not db_breed:
        return None

    # Obtém os dados do schema de atualização como um dicionário
    update_data = breed_update.model_dump(exclude_unset=True)

    # Itera sobre os dados e atualiza os campos do objeto SQLAlchemy
    for key, value in update_data.items():
        setattr(db_breed, key, value)

    db.add(db_breed)
    db.commit()
    db.refresh(db_breed)
    return db_breed


def delete_breed(db: Session, breed_id: UUID) -> models.Breed | None:
    """
    Remove uma raça do banco de dados pelo seu ID.
    """
    db_breed = get_breed_by_id(db, breed_id=breed_id)
    if not db_breed:
        return None

    # Adicionamos uma verificação para não apagar a raça "SRD (Sem Raça Definida)"
    if db_breed.name == "SRD (Sem Raça Definida)":
        return None  # Ou levantar uma exceção, dependendo da regra de negócio

    db.delete(db_breed)
    db.commit()
    return db_breed
