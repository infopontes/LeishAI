from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict


# --- Schemas Base ---
# Campos compartilhados por outros schemas para evitar repetição
class UserBase(BaseModel):
    email: EmailStr


# --- Schema para Criação ---
# Campos necessários para criar um novo usuário (recebidos via API)
class UserCreate(UserBase):
    password: str


# --- Schema para Leitura ---
# Campos que serão retornados pela API (NUNCA inclua a senha!)
class UserPublic(UserBase):
    id: UUID
    is_active: bool

    # Configuração para permitir que o Pydantic leia dados de um modelo ORM (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)
