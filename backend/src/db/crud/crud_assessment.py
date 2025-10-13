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


def get_assessment_by_id(
    db: Session, assessment_id: UUID
) -> models.Assessment | None:
    """
    Busca um atendimento pelo seu ID.
    """
    return (
        db.query(models.Assessment)
        .filter(models.Assessment.id == assessment_id)
        .first()
    )


def update_assessment(
    db: Session,
    assessment_id: UUID,
    assessment_update: assessment_schema.AssessmentUpdate,
) -> models.Assessment | None:
    """
    Atualiza os dados de um atendimento existente.
    """
    db_assessment = get_assessment_by_id(db, assessment_id=assessment_id)
    if not db_assessment:
        return None

    # Obtém os dados do schema de atualização como um dicionário
    update_data = assessment_update.model_dump(exclude_unset=True)

    # Itera sobre os dados e atualiza os campos do objeto SQLAlchemy
    for key, value in update_data.items():
        setattr(db_assessment, key, value)

    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment


def delete_assessment(
    db: Session, assessment_id: UUID
) -> models.Assessment | None:
    """
    Remove um atendimento do banco de dados pelo seu ID.
    """
    db_assessment = get_assessment_by_id(db, assessment_id=assessment_id)
    if not db_assessment:
        return None

    db.delete(db_assessment)
    db.commit()
    return db_assessment
