from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db import crud
from src.db.database import SessionLocal
from src.schemas import user as user_schema

router = APIRouter(prefix="/users", tags=["Users"])


# Função de dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=user_schema.UserPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_new_user(
    user: user_schema.UserCreate, db: Session = Depends(get_db)
):
    """
    Cria um novo usuário no sistema.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return crud.create_user(db=db, user=user)
