from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.db.crud import crud_user
from src.schemas.user import UserCreate


SUCCESS_MESSAGE = (
    "If the account exists, we've sent password reset instructions."
)


def test_forgot_password_returns_ok_for_existing_user(
    client: TestClient, db_session: Session
):
    user_in = UserCreate(
        email="existing@example.com",
        password="password123",
        full_name="Existing User",
    )
    user = crud_user.create_user(db_session, user=user_in)
    user.is_active = True
    db_session.commit()

    response = client.post(
        "/auth/forgot-password", json={"email": user.email}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == SUCCESS_MESSAGE


def test_forgot_password_returns_ok_for_unknown_email(
    client: TestClient, db_session: Session
):
    response = client.post(
        "/auth/forgot-password", json={"email": "unknown@example.com"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == SUCCESS_MESSAGE
