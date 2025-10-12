from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.crud import crud_breed
from src.schemas import breed as breed_schema
from .dependencies import get_current_user, get_db
from .router_roles import (
    get_current_admin_user,
)  # Reutilizando a dependência de admin

router = APIRouter(prefix="/breeds", tags=["Breeds"])


@router.post(
    "/",
    response_model=breed_schema.BreedPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(get_current_admin_user)
    ],  # 👈 Apenas admins podem criar
)
def create_new_breed(
    breed: breed_schema.BreedCreate, db: Session = Depends(get_db)
):
    """
    Cria uma nova raça no sistema.
    Apenas para usuários administradores.
    """
    db_breed = crud_breed.get_breed_by_name(db, name=breed.name)
    if db_breed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Breed '{breed.name}' already exists.",
        )
    return crud_breed.create_breed(db=db, breed=breed)


@router.get(
    "/",
    response_model=List[breed_schema.BreedPublic],
    dependencies=[
        Depends(get_current_user)
    ],  # 👈 Qualquer usuário logado pode listar
)
def read_breeds(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retorna uma lista de raças.
    Acessível para qualquer usuário logado.
    """
    breeds = crud_breed.get_breeds(db, skip=skip, limit=limit)
    return breeds
