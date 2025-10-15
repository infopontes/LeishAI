import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from src.core.config import settings
from src.main import app


@pytest.fixture(scope="function", autouse=True)
def override_test_settings(monkeypatch):
    """
    Forces 'TESTING' to be set to True BEFORE EACH TEST.
    'Scope="function"' resolves the ScopeMismatch error.
    'Autouse=True' ensures this fixture runs automatically.
    """
    monkeypatch.setattr(settings, "TESTING", True)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=create_engine(settings.DATABASE_URL),
)


@pytest.fixture(scope="session")
def client():
    """
    Provides a TestClient that is created once per test session.
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def db_session():
    """
    Provides a clean database session for each test function.
    """
    engine = create_engine(settings.DATABASE_URL)
    with engine.connect() as connection:
        with connection.begin():
            # Clears all tables before each test to ensure isolation
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
