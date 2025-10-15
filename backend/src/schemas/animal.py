import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict

# Import the public schemas we created
from .owner import OwnerPublic
from .breed import BreedPublic


# Shared fields
class AnimalBase(BaseModel):
    name: str
    original_id: Optional[str] = None
    sex: Optional[str] = None


# Schema for creating an animal.
# Note that we receive the owner and breed IDs.
class AnimalCreate(AnimalBase):
    owner_id: uuid.UUID
    breed_id: uuid.UUID


# Schema for updating. Fields like owner_id and breed_id are optional when updating.
class AnimalUpdate(AnimalBase):
    pass


# Schema to return in the API.
# Note that the 'owner' and 'breed' fields use the public schemas.
class AnimalPublic(AnimalBase):
    id: uuid.UUID
    owner: OwnerPublic
    breed: BreedPublic
    model_config = ConfigDict(from_attributes=True)
