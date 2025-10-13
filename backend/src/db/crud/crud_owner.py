from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from src.db import models
from src.schemas import owner as owner_schema


def get_owner_by_id(db: Session, owner_id: UUID) -> models.Owner | None:
    return db.query(models.Owner).filter(models.Owner.id == owner_id).first()


def create_owner(db: Session, owner: owner_schema.OwnerCreate) -> models.Owner:
    db_owner = models.Owner(**owner.model_dump())
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner


def get_owners(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.Owner]:
    return db.query(models.Owner).offset(skip).limit(limit).all()


def get_owner_by_name(db: Session, name: str) -> models.Owner | None:
    """
    Busca um proprietário pelo seu nome (case-insensitive).
    """
    return db.query(models.Owner).filter(models.Owner.name.ilike(name)).first()


def update_owner(
    db: Session, owner_id: UUID, owner_update: owner_schema.OwnerCreate
) -> models.Owner | None:
    """
    Atualiza os dados de um proprietário existente.
    """
    db_owner = get_owner_by_id(db, owner_id=owner_id)
    if not db_owner:
        return None

    # Obtém os dados do schema de atualização como um dicionário
    update_data = owner_update.model_dump(exclude_unset=True)

    # Itera sobre os dados e atualiza os campos do objeto SQLAlchemy
    for key, value in update_data.items():
        setattr(db_owner, key, value)

    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner


def delete_owner(db: Session, owner_id: UUID) -> models.Owner | None:
    """
    Remove um proprietário do banco de dados pelo seu ID.
    """
    db_owner = get_owner_by_id(db, owner_id=owner_id)
    if not db_owner:
        return None

    db.delete(db_owner)
    db.commit()
    return db_owner
