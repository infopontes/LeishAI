import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict

# Importa os schemas públicos que criamos
from .owner import OwnerPublic
from .breed import BreedPublic


# Campos compartilhados
class AnimalBase(BaseModel):
    name: str
    original_id: Optional[str] = None
    sex: Optional[str] = None


# Schema para criação de um animal.
# Note que recebemos os IDs do proprietário e da raça.
class AnimalCreate(AnimalBase):
    owner_id: uuid.UUID
    breed_id: uuid.UUID


# Schema para atualização. Campos como owner_id e breed_id são opcionais na atualização.
class AnimalUpdate(AnimalBase):
    pass


# Schema para retorno na API.
# Note que os campos 'owner' e 'breed' usam os schemas públicos.
class AnimalPublic(AnimalBase):
    id: uuid.UUID
    owner: OwnerPublic
    breed: BreedPublic
    model_config = ConfigDict(from_attributes=True)
