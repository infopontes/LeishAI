import uuid
from pydantic import BaseModel, ConfigDict


# Campos compartilhados
class BreedBase(BaseModel):
    name: str


# Schema para criação
class BreedCreate(BreedBase):
    pass


# Schema para retorno na API
class BreedPublic(BreedBase):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)
