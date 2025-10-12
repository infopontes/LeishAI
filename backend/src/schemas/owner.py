import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict


# Campos compartilhados
class OwnerBase(BaseModel):
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None


# Schema para criação de um proprietário
class OwnerCreate(OwnerBase):
    pass


# Schema para retorno na API (inclui o ID)
class OwnerPublic(OwnerBase):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)
