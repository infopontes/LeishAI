from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from fastapi import Response

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
    Creates a new appointment (clinical evaluation) for an animal.
    The appointment is associated with the user (veterinarian) making the request.
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
    Returns a list of appointments.
    """
    assessments = crud_assessment.get_assessments(db, skip=skip, limit=limit)
    return assessments


@router.get(
    "/{assessment_id}",
    response_model=assessment_schema.AssessmentPublic,
    dependencies=[Depends(get_current_user)],
)
def read_assessment_by_id(assessment_id: UUID, db: Session = Depends(get_db)):
    """
    Search for a single service using your ID.
    """
    db_assessment = crud_assessment.get_assessment_by_id(
        db, assessment_id=assessment_id
    )
    if db_assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )
    return db_assessment


@router.put(
    "/{assessment_id}",
    response_model=assessment_schema.AssessmentPublic,
    dependencies=[Depends(get_current_user)],
)
def update_existing_assessment(
    assessment_id: UUID,
    assessment_update: assessment_schema.AssessmentUpdate,
    db: Session = Depends(get_db),
):
    """
    Updates the data of an existing service.
    """
    db_assessment = crud_assessment.update_assessment(
        db=db, assessment_id=assessment_id, assessment_update=assessment_update
    )
    if db_assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )
    return db_assessment


@router.delete(
    "/{assessment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_user)],
)
def delete_existing_assessment(
    assessment_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Removes an existing service.
    """
    deleted_assessment = crud_assessment.delete_assessment(
        db=db, assessment_id=assessment_id
    )
    if deleted_assessment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
