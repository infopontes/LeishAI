from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

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
