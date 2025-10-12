import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Breed(Base):
    __tablename__ = "breeds"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True, nullable=False)

    # Relacionamento: Uma raça pode ter vários animais
    animals = relationship("Animal", back_populates="breed")
