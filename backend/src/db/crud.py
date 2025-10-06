from sqlalchemy.orm import Session
from . import models
from src.schemas import user as user_schema
from src.core.security import get_password_hash


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: user_schema.UserCreate):
    # Verifica se a senha ultrapassa 72 bytes em UTF-8 (limite do bcrypt)
    if len(user.password.encode("utf-8")) > 72:
        raise ValueError("Password too long — bcrypt supports up to 72 bytes.")

    # Gera o hash da senha
    hashed_password = get_password_hash(user.password)

    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
