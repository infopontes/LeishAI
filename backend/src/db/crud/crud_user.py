from sqlalchemy.orm import Session
from typing import List
from src.db import models
from src.schemas import user as user_schema, role as role_schema
from src.core.security import get_password_hash, verify_password
from . import crud_role


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: user_schema.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)

    default_role = crud_role.get_role_by_name(db, name="veterinario")
    if not default_role:
        default_role = crud_role.create_role(
            db,
            role_schema.RoleCreate(
                name="veterinario",
                description="Usuário com permissões para gerenciar atendimentos.",
            ),
        )

    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        institution=user.institution,
        role_id=default_role.id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(
    db: Session, email: str, password: str
) -> models.User | None:
    user = get_user_by_email(db, email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def get_users(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()
