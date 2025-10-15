import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict


# Shared fields
class OwnerBase(BaseModel):
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    neighborhood: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None


# Schema for creating an owner
class OwnerCreate(OwnerBase):
    pass


# Schema to return in the API (includes the ID)
class OwnerPublic(OwnerBase):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)
