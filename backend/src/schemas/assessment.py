import uuid
from pydantic import BaseModel, ConfigDict
from src.db.models import enums  # Importa nossos Enums

# Importa os schemas públicos
from .animal import AnimalPublic
from .user import UserPublic


# Campos compartilhados
class AssessmentBase(BaseModel):
    original_id: str | None = None
    general_state: enums.GeneralState | None = None
    ectoparasites: enums.Severity | None = None
    nutritional_state: enums.NutritionalState | None = None
    coat: enums.LesionSeverity | None = None
    nails: enums.LesionSeverity | None = None
    mucosa_color: enums.MucosaColor | None = None
    muzzle_ear_lesion: enums.PresenceAbsence | None = None
    lymph_nodes: enums.LesionSeverity | None = None
    blepharitis: enums.PresenceAbsence | None = None
    conjunctivitis: enums.PresenceAbsence | None = None
    alopecia: enums.PresenceAbsence | None = None
    bleeding: enums.PresenceAbsence | None = None
    skin_lesion: enums.PresenceAbsence | None = None
    muzzle_lip_depigmentation: enums.PresenceAbsence | None = None
    culture: enums.DiagnosisResult | None = None
    slide: enums.DiagnosisResult | None = None
    diagnosis: enums.DiagnosisResult | None = None


# Schema para criação de um atendimento.
# Recebemos o ID do animal. O ID do usuário virá do token de autenticação.
class AssessmentCreate(AssessmentBase):
    animal_id: uuid.UUID


# Schema para retorno na API.
# Inclui os objetos aninhados de animal e user.
class AssessmentPublic(AssessmentBase):
    id: uuid.UUID
    animal: AnimalPublic
    user: UserPublic
    model_config = ConfigDict(from_attributes=True)
