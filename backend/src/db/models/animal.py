import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Animal(Base):
    __tablename__ = "animals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_id = Column(String, unique=True, index=True, nullable=True)
    name = Column(String, index=True, nullable=False)
    sex = Column(String(1), nullable=True)

    breed_id = Column(
        UUID(as_uuid=True), ForeignKey("breeds.id"), nullable=False
    )
    owner_id = Column(
        UUID(as_uuid=True), ForeignKey("owners.id"), nullable=False
    )

    breed = relationship("Breed", back_populates="animals")
    owner = relationship("Owner", back_populates="animals")
    assessments = relationship("Assessment", back_populates="animal")
