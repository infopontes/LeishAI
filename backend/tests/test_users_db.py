import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db import crud
from src.core.config import settings

# Usamos um banco de dados de teste, se necessário, mas por agora o mesmo serve
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=create_engine(settings.DATABASE_URL),
)


# Fixture para fornecer uma sessão de banco de dados para os testes
@pytest.fixture()
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_and_retrieve_user(db_session):
    """
    Testa a criação e a busca de um usuário no banco de dados.
    """
    user_email = "test@example.com"
    user_password = "testpassword123"

    # 1. Tenta criar um usuário (vai falhar)
    db_user = crud.create_user(
        db=db_session, email=user_email, password=user_password
    )
    assert db_user.email == user_email

    # 2. Tenta buscar o usuário pelo email (vai falhar)
    retrieved_user = crud.get_user_by_email(db=db_session, email=user_email)

    assert retrieved_user
    assert retrieved_user.email == user_email
    assert retrieved_user.id == db_user.id
