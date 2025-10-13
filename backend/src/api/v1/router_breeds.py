from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import Response

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


@router.get(
    "/{breed_id}",
    response_model=breed_schema.BreedPublic,
    dependencies=[
        Depends(get_current_user)
    ],  # Qualquer utilizador logado pode ver
)
def read_breed_by_id(breed_id: UUID, db: Session = Depends(get_db)):
    """
    Busca uma única raça pelo seu ID.
    """
    db_breed = crud_breed.get_breed_by_id(db, breed_id=breed_id)
    if db_breed is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Breed not found",
        )
    return db_breed


@router.put(
    "/{breed_id}",
    response_model=breed_schema.BreedPublic,
    dependencies=[
        Depends(get_current_admin_user)
    ],  # Apenas admins podem atualizar
)
def update_existing_breed(
    breed_id: UUID,
    breed_update: breed_schema.BreedCreate,  # Reutilizamos o schema de criação
    db: Session = Depends(get_db),
):
    """
    Atualiza os dados de uma raça existente.
    """
    # Verifica se a raça com o novo nome já existe para evitar duplicatas
    existing_breed = crud_breed.get_breed_by_name(db, name=breed_update.name)
    if existing_breed and existing_breed.id != breed_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Breed with name '{breed_update.name}' already exists.",
        )

    db_breed = crud_breed.update_breed(
        db=db, breed_id=breed_id, breed_update=breed_update
    )
    if db_breed is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Breed not found",
        )
    return db_breed


@router.delete(
    "/{breed_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(get_current_admin_user)
    ],  # Apenas admins podem apagar
)
def delete_existing_breed(
    breed_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Remove uma raça existente.
    """
    # Adicionamos uma verificação de dependência: não permitir apagar uma raça se houver animais associados a ela.
    db_breed = crud_breed.get_breed_by_id(db, breed_id=breed_id)
    if not db_breed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Breed not found",
        )

    if (
        db_breed.animals
    ):  # Verifica se a lista de animais da raça não está vazia
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete breed with associated animals.",
        )

    crud_breed.delete_breed(db=db, breed_id=breed_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
