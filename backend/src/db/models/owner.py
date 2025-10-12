import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .base import Base


class Owner(Base):
    __tablename__ = "owners"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, index=True, nullable=False)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    neighborhood = Column(String, nullable=True)  # bairro
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)  # uf

    # Relacionamento: Um proprietário pode ter vários animais.
    # 'animals' será uma lista de objetos Animal.
    animals = relationship("Animal", back_populates="owner")
