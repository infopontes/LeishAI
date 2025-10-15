import uuid
from sqlalchemy import Column, String, ForeignKey, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from . import enums


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_id = Column(String, nullable=True)

    # Clinical fields
    general_state = Column(Enum(enums.GeneralState), nullable=True)
    ectoparasites = Column(Enum(enums.Severity), nullable=True)
    nutritional_state = Column(Enum(enums.NutritionalState), nullable=True)
    coat = Column(Enum(enums.LesionSeverity), nullable=True)
    nails = Column(Enum(enums.LesionSeverity), nullable=True)
    mucosa_color = Column(Enum(enums.MucosaColor), nullable=True)
    muzzle_ear_lesion = Column(Enum(enums.PresenceAbsence), nullable=True)
    lymph_nodes = Column(Enum(enums.LesionSeverity), nullable=True)
    blepharitis = Column(Enum(enums.PresenceAbsence), nullable=True)
    conjunctivitis = Column(String, nullable=True)  # 👈 Alterado para String
    alopecia = Column(Enum(enums.PresenceAbsence), nullable=True)
    bleeding = Column(Enum(enums.PresenceAbsence), nullable=True)
    skin_lesion = Column(String, nullable=True)  # 👈 Alterado para String
    muzzle_lip_depigmentation = Column(
        Enum(enums.PresenceAbsence), nullable=True
    )

    # Laboratory results
    culture = Column(Enum(enums.DiagnosisResult), nullable=True)
    slide = Column(Enum(enums.DiagnosisResult), nullable=True)
    diagnosis = Column(Enum(enums.DiagnosisResult), nullable=True)

    # Foreign keys
    animal_id = Column(
        UUID(as_uuid=True), ForeignKey("animals.id"), nullable=False
    )
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    # Relationships
    animal = relationship("Animal", back_populates="assessments")
    user = relationship("User", back_populates="assessments")

    # Audit
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
