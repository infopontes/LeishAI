from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from src.db import models
from src.schemas import user as user_schema, role as role_schema
from src.core.security import get_password_hash, verify_password
from . import crud_role

def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: UUID) -> models.User | None:
    """Busca um utilizador pelo seu ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: user_schema.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    
    default_role = crud_role.get_role_by_name(db, name="veterinario")
    if not default_role:
        default_role = crud_role.create_role(
            db, 
            role_schema.RoleCreate(
                name="veterinario", 
                description="Usuário com permissões para gerenciar atendimentos."
            )
        )
        
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        institution=user.institution,
        role_id=default_role.id,
        is_active=False  # 👈 **CORREÇÃO PRINCIPAL: Definição explícita**
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ... (o resto das funções, como update_user, authenticate_user, etc., continuam iguais)
def update_user(db: Session, user_id: UUID, user_update: user_schema.UserUpdateAdmin) -> models.User | None:
    # ...
    db_user = get_user_by_id(db, user_id=user_id)
    if not db_user:
        return None
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> models.User | None:
    user = get_user_by_email(db, email=email)
    if not user or not verify_password(password, user.hashed_password) or not user.is_active:
        return None
    return user

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

def deactivate_user(db: Session, user_id: UUID) -> models.User | None:
    db_user = get_user_by_id(db, user_id=user_id)
    if not db_user:
        return None
    db_user.is_active = False
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user