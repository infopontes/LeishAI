import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Importe 'settings' para podermos modificá-lo
from src.core.config import settings
from src.main import app

# --- INÍCIO DA CORREÇÃO DEFINITIVA ---


@pytest.fixture(scope="function", autouse=True)
def override_test_settings(monkeypatch):
    """
    Força a configuração de 'TESTING' para True ANTES DE CADA TESTE.
    O 'scope="function"' resolve o erro de ScopeMismatch.
    'autouse=True' garante que esta fixture é executada automaticamente.
    """
    monkeypatch.setattr(settings, "TESTING", True)


# --- FIM DA CORREÇÃO DEFINITIVA ---


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=create_engine(settings.DATABASE_URL),
)


@pytest.fixture(scope="session")
def client():
    """
    Fornece um TestClient que é criado uma vez por sessão de teste.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def db_session():
    """
    Fornece uma sessão de banco de dados limpa para cada função de teste.
    """
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as connection:
        with connection.begin():
            # Limpa todas as tabelas antes de cada teste para garantir isolamento
            connection.execute(
                text(
                    "TRUNCATE TABLE users, roles, owners, breeds, animals, assessments RESTART IDENTITY CASCADE;"
                )
            )

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
