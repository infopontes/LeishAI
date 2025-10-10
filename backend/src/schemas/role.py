import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict


class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    pass


class RolePublic(RoleBase):
    id: uuid.UUID
    model_config = ConfigDict(from_attributes=True)
