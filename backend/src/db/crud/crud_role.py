from typing import List
from sqlalchemy.orm import Session
from src.db import models
from src.schemas import role as role_schema


def create_role(db: Session, role: role_schema.RoleCreate) -> models.Role:
    db_role = models.Role(name=role.name, description=role.description)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def get_role_by_name(db: Session, name: str) -> models.Role | None:
    return db.query(models.Role).filter(models.Role.name == name).first()


def get_roles(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.Role]:
    return db.query(models.Role).offset(skip).limit(limit).all()
