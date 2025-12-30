from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.db.crud import crud_user
from src.schemas.user import UserCreate
from src.core import security
from src.core.config import settings
from jose import jwt
import uuid
import pytest


SUCCESS_MESSAGE = (
    "If the account exists, we've sent password reset instructions."
)


def test_forgot_password_sends_email_for_existing_active_user(
    client: TestClient, db_session: Session, monkeypatch
):
    sent_payload = {}

    def fake_send_email(to_email: str, reset_url: str):
        sent_payload["to"] = to_email
        sent_payload["reset_url"] = reset_url
        return True

    user_in = UserCreate(
        email="existing@example.com",
        password="password123",
        full_name="Existing User",
    )
    user = crud_user.create_user(db_session, user=user_in)
    user.is_active = True
    db_session.commit()

    monkeypatch.setattr(
        "src.api.v1.router_auth.send_password_reset_email", fake_send_email
    )

    response = client.post(
        "/auth/forgot-password", json={"email": user.email}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == SUCCESS_MESSAGE
    assert sent_payload["to"] == user.email
    token = sent_payload["reset_url"].split("token=")[-1]
    decoded = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert decoded["sub"] == user.email
    assert decoded["scope"] == "password_reset"


def test_forgot_password_returns_ok_for_unknown_email(
    client: TestClient, db_session: Session, monkeypatch
):
    called = False

    def fake_send_email(*args, **kwargs):
        nonlocal called
        called = True
        return True

    monkeypatch.setattr(
        "src.api.v1.router_auth.send_password_reset_email", fake_send_email
    )

    response = client.post(
        "/auth/forgot-password", json={"email": "unknown@example.com"}
    )

    assert response.status_code == 200
    assert response.json()["detail"] == SUCCESS_MESSAGE
    assert called is False


def test_reset_password_success(client: TestClient, db_session: Session):
    new_password = "newpass123!"
    user_in = UserCreate(
        email="resetme@example.com",
        password="oldpass",
        full_name="Reset Me",
    )
    user = crud_user.create_user(db_session, user=user_in)
    user.is_active = True
    db_session.commit()

    token = security.create_password_reset_token(user.email)
    response = client.post(
        "/auth/reset-password",
        json={"token": token, "new_password": new_password},
    )

    assert response.status_code == 200
    assert response.json()["detail"] == "Password updated successfully"

    login_response = client.post(
        "/auth/token", data={"username": user.email, "password": new_password}
    )
    assert login_response.status_code == 200


@pytest.mark.parametrize(
    "token",
    [
        "invalid-token",
        security.create_access_token({"sub": "foo", "scope": "wrong"}),
    ],
)
def test_reset_password_invalid_token(client: TestClient, token):
    response = client.post(
        "/auth/reset-password",
        json={"token": token, "new_password": "whatever"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid or expired token"


def test_reset_password_rejects_short_password(
    client: TestClient, db_session: Session
):
    user_in = UserCreate(
        email="shortpass@example.com",
        password="oldpass",
        full_name="Short Pass",
    )
    user = crud_user.create_user(db_session, user=user_in)
    user.is_active = True
    db_session.commit()

    token = security.create_password_reset_token(user.email)
    response = client.post(
        "/auth/reset-password",
        json={"token": token, "new_password": "123"},
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "string_too_short"
