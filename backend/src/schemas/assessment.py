import uuid
from pydantic import BaseModel, ConfigDict
from src.db.models import enums

from .animal import AnimalPublic
from .user import UserPublic


class AssessmentBase(BaseModel):
    general_state: enums.GeneralState | None = None
    ectoparasites: enums.Severity | None = None
    nutritional_state: enums.NutritionalState | None = None
    coat: enums.LesionSeverity | None = None
    nails: enums.LesionSeverity | None = None
    mucosa_color: enums.MucosaColor | None = None
    muzzle_ear_lesion: enums.PresenceAbsence | None = None
    lymph_nodes: enums.LesionSeverity | None = None
    blepharitis: enums.PresenceAbsence | None = None
    conjunctivitis: str | None = None  # 👈 Alterado para str
    alopecia: enums.PresenceAbsence | None = None
    bleeding: enums.PresenceAbsence | None = None
    skin_lesion: str | None = None  # 👈 Alterado para str
    muzzle_lip_depigmentation: enums.PresenceAbsence | None = None
    culture: enums.DiagnosisResult | None = None
    slide: enums.DiagnosisResult | None = None
    diagnosis: enums.DiagnosisResult | None = None


class AssessmentCreate(AssessmentBase):
    animal_id: uuid.UUID


class AssessmentPublic(AssessmentBase):
    id: uuid.UUID
    animal: AnimalPublic
    user: UserPublic
    model_config = ConfigDict(from_attributes=True)
