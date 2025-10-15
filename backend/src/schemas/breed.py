import uuid
from pydantic import BaseModel, ConfigDict


# Shared fields
class BreedBase(BaseModel):
    name: str


# Schema for creation
class BreedCreate(BreedBase):
    pass


# Schema for return in API
class BreedPublic(BreedBase):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)
