from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.db.crud import crud_role
from src.schemas import role as role_schema
from .dependencies import get_current_user, get_db, get_current_admin_user

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post(
    "/",
    response_model=role_schema.RolePublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin_user)],
)
def create_new_role(
    role: role_schema.RoleCreate, db: Session = Depends(get_db)
):
    """
    Cria uma nova role.
    Apenas administradores podem criar roles.
    """
    db_role = crud_role.get_role_by_name(db, name=role.name)
    if db_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role with this name already exists",
        )
    new_role = crud_role.create_role(db=db, role=role)
    return role_schema.RolePublic.from_orm(new_role)


@router.get(
    "/",
    response_model=List[role_schema.RolePublic],
    dependencies=[Depends(get_current_user)],
)
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lista todas as roles.
    Usuários autenticados podem visualizar.
    """
    roles = crud_role.get_roles(db, skip=skip, limit=limit)
    return [role_schema.RolePublic.from_orm(r) for r in roles]
