from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from src.db.crud import crud_assessment
from src.schemas import assessment as assessment_schema
from src.db import models
from .dependencies import get_current_user, get_db

router = APIRouter(prefix="/assessments", tags=["Assessments"])


@router.post(
    "/",
    response_model=assessment_schema.AssessmentPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_new_assessment(
    assessment: assessment_schema.AssessmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        get_current_user
    ),  # 👈 Obtém o usuário logado
):
    """
    Cria um novo atendimento (avaliação clínica) para um animal.
    O atendimento é associado ao usuário (veterinário) que está fazendo a requisição.
    """
    return crud_assessment.create_assessment(
        db=db, assessment=assessment, user_id=current_user.id
    )


@router.get(
    "/",
    response_model=List[assessment_schema.AssessmentPublic],
    dependencies=[Depends(get_current_user)],
)
def read_assessments(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """
    Retorna uma lista de atendimentos.
    """
    assessments = crud_assessment.get_assessments(db, skip=skip, limit=limit)
    return assessments
