from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
from src.db import models
from src.schemas import assessment as assessment_schema


def create_assessment(
    db: Session, assessment: assessment_schema.AssessmentCreate, user_id: UUID
) -> models.Assessment:
    """
    Creates a new service in the database.
    """
    # model_dump() converte o schema Pydantic para um dicionário
    db_assessment = models.Assessment(
        **assessment.model_dump(),
        user_id=user_id,  # Adds the logged in user ID
    )
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment


def get_assessments(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.Assessment]:
    """
    Search for a list of services with pagination.
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
    Search for assistance using your ID.
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
    Updates the data of an existing service.
    """
    db_assessment = get_assessment_by_id(db, assessment_id=assessment_id)
    if not db_assessment:
        return None

    # Gets the update schema data as a dictionary
    update_data = assessment_update.model_dump(exclude_unset=True)

    # Iterates over the data and updates the fields of the SQLAlchemy object
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
    Removes a service from the database by its ID.
    """
    db_assessment = get_assessment_by_id(db, assessment_id=assessment_id)
    if not db_assessment:
        return None

    db.delete(db_assessment)
    db.commit()
    return db_assessment
