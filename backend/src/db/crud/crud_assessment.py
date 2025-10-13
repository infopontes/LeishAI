from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
from src.db import models
from src.schemas import assessment as assessment_schema


def create_assessment(
    db: Session, assessment: assessment_schema.AssessmentCreate, user_id: UUID
) -> models.Assessment:
    """
    Cria um novo atendimento no banco de dados.
    """
    # model_dump() converte o schema Pydantic para um dicionário
    db_assessment = models.Assessment(
        **assessment.model_dump(),
        user_id=user_id,  # Adiciona o ID do usuário logado
    )
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment


def get_assessments(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.Assessment]:
    """
    Busca uma lista de atendimentos com paginação.
    """
    return (
        db.query(models.Assessment)
        .order_by(models.Assessment.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
