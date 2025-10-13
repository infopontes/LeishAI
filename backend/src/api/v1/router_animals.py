from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import Response

from src.db.crud import crud_animal
from src.schemas import animal as animal_schema
from .dependencies import get_current_user, get_db
from typing import List

router = APIRouter(prefix="/animals", tags=["Animals"])


@router.post(
    "/",
    response_model=animal_schema.AnimalPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],  # 👈 A rota é protegida
)
def create_new_animal(
    animal: animal_schema.AnimalCreate, db: Session = Depends(get_db)
):
    """
    Cria um novo animal no sistema, associado a um proprietário e a uma raça.
    """
    # Futuramente, poderíamos adicionar verificações aqui, como se o owner_id
    # e o breed_id realmente existem, antes de tentar criar.
    return crud_animal.create_animal(db=db, animal=animal)


@router.get(
    "/",
    response_model=List[animal_schema.AnimalPublic],
    dependencies=[Depends(get_current_user)],
)
def read_animals(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retorna uma lista de animais.
    """
    animals = crud_animal.get_animals(db, skip=skip, limit=limit)
    return animals


@router.get(
    "/{animal_id}",
    response_model=animal_schema.AnimalPublic,
    dependencies=[
        Depends(get_current_user)
    ],  # Qualquer utilizador logado pode ver
)
def read_animal_by_id(animal_id: UUID, db: Session = Depends(get_db)):
    """
    Busca um único animal pelo seu ID.
    """
    db_animal = crud_animal.get_animal_by_id(db, animal_id=animal_id)
    if db_animal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal not found",
        )
    return db_animal


@router.put(
    "/{animal_id}",
    response_model=animal_schema.AnimalPublic,
    dependencies=[Depends(get_current_user)],
)
def update_existing_animal(
    animal_id: UUID,
    animal_update: animal_schema.AnimalUpdate,  # Usamos o novo schema de atualização
    db: Session = Depends(get_db),
):
    """
    Atualiza os dados de um animal existente.
    """
    db_animal = crud_animal.update_animal(
        db=db, animal_id=animal_id, animal_update=animal_update
    )
    if db_animal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal not found",
        )
    return db_animal


@router.delete(
    "/{animal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
def delete_existing_animal(
    animal_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Remove um animal existente.
    """
    # Adicionamos uma verificação de dependência: não permitir apagar um animal se houver atendimentos associados a ele.
    db_animal = crud_animal.get_animal_by_id(db, animal_id=animal_id)
    if not db_animal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Animal not found",
        )

    if (
        db_animal.assessments
    ):  # Verifica se a lista de atendimentos do animal não está vazia
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete animal with associated assessments.",
        )

    crud_animal.delete_animal(db=db, animal_id=animal_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
