from sqlalchemy.orm import Session
from . import models
from src.schemas import user as user_schema
from src.core.security import get_password_hash, verify_password


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: user_schema.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    """
    Verifica se um usuário existe e se a senha está correta.
    """
    # 1. Busca o usuário pelo e-mail
    user = get_user_by_email(db, email=email)

    # 2. Se não encontrar o usuário, retorna False
    if not user:
        return False

    # 3. Se encontrou, verifica se a senha enviada corresponde à senha com hash do banco
    if not verify_password(password, user.hashed_password):
        return False

    # 4. Se a senha estiver correta, retorna o objeto do usuário
    return user
