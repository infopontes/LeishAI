from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from .test_utils import get_authenticated_headers
from src.schemas import user as user_schema
from src.db.crud import crud_user, crud_role
from src.schemas.role import RoleCreate
from src.core import security
from src.core.config import settings
from src.services import email as email_service


def test_read_users_as_admin(client: TestClient, db_session: Session):
    """
    Tests the listing of all users by an administrator user.
    """
    # Create a regular user to ensure the list is not empty
    get_authenticated_headers(client, db_session, "common_user@example.com")

    # Gets headers for an admin user
    admin_headers = get_authenticated_headers(
        client, db_session, "admin_for_test@example.com", role_name="admin"
    )

    # Make the request to the endpoint we want to create
    response = client.get("/users/", headers=admin_headers)

    # Assertions
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # There must be at least admin and regular user


def test_read_users_as_non_admin_fails(
    client: TestClient, db_session: Session
):
    """
    Tests that a non-admin user cannot list all users.
    """
    # Gets headers for a user with 'veterinario' profile
    vet_headers = get_authenticated_headers(
        client, db_session, "vet_for_test@example.com", role_name="veterinario"
    )

    # Makes the request to the same endpoint
    response = client.get("/users/", headers=vet_headers)

    # Assertion: We expect a 403 Forbidden error
    assert response.status_code == 403, response.text
    assert (
        response.json()["detail"] == "The user does not have enough privileges"
    )


def test_update_user_as_admin(client: TestClient, db_session: Session):
    """
    Tests whether an admin can update another user's name and profile.
    """
    # 1. Create the admin user and the target user
    admin_headers = get_authenticated_headers(
        client, db_session, "admin_to_update@example.com", role_name="admin"
    )
    target_user_in = user_schema.UserCreate(
        email="target@example.com",
        password="password",
        full_name="Nome Antigo",
    )
    target_user = crud_user.create_user(db_session, user=target_user_in)

    # 2. Create the new profile to which we will switch the user
    new_role_in = RoleCreate(
        name="coordenador_teste", description="Perfil de Teste"
    )
    new_role = crud_role.create_role(db_session, role=new_role_in)

    # 3. Data for the update
    update_data = {
        "full_name": "Nome Novo Atualizado",
        "institution": "Nova Instituição",
        "role_id": str(new_role.id),  # We convert the UUID to string for JSON
    }

    # 4. Make the PUT request
    response = client.put(
        f"/users/{target_user.id}", headers=admin_headers, json=update_data
    )

    # 5. Assertions
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["full_name"] == update_data["full_name"]
    assert data["institution"] == update_data["institution"]
    assert data["role"]["id"] == update_data["role_id"]


def test_update_user_as_non_admin_fails(
    client: TestClient, db_session: Session
):
    """
    Tests that a non-admin user cannot update another user.
    """
    # 1. Create the non-admin user and the target user
    vet_headers = get_authenticated_headers(
        client,
        db_session,
        "vet_cant_update@example.com",
        role_name="veterinario",
    )
    target_user_in = user_schema.UserCreate(
        email="another_target@example.com",
        password="password",
        full_name="Nome Alvo",
    )
    target_user = crud_user.create_user(db_session, user=target_user_in)

    # 2. Update data (should not be applied)
    update_data = {"full_name": "Nome que não deve ser atualizado"}

    # 3. Make the PUT request
    response = client.put(
        f"/users/{target_user.id}", headers=vet_headers, json=update_data
    )

    # 4. Assertion
    assert response.status_code == 403


def test_deactivate_user_as_admin(client: TestClient, db_session: Session):
    """
    Tests the deactivation ('soft delete') of a user by an administrator.
    """
    admin_headers = get_authenticated_headers(
        client, db_session, "admin_for_delete@example.com", role_name="admin"
    )
    target_user_in = user_schema.UserCreate(
        email="user_to_deactivate@example.com",
        password="password",
        full_name="Utilizador a Desativar",
    )
    target_user = crud_user.create_user(db_session, user=target_user_in)
    assert target_user.is_active is False

    # Activate the user before you can deactivate them
    target_user.is_active = True
    db_session.commit()
    db_session.refresh(target_user)
    assert target_user.is_active is True

    # Make the DELETE request
    response_delete = client.delete(
        f"/users/{target_user.id}", headers=admin_headers
    )

    assert response_delete.status_code == 204

    # Check if it has been disabled
    db_session.refresh(target_user)
    assert target_user.is_active is False

    # Try to log in and check if it fails
    login_data = {
        "username": "user_to_deactivate@example.com",
        "password": "password",
    }
    response_login = client.post("/auth/token", data=login_data)
    assert response_login.status_code == 401


def test_create_user_sends_activation_email(
    client: TestClient, db_session: Session, monkeypatch
):
    sent = {}

    def fake_send_user_activation_email(
        admin_email: str, activation_url: str, user_email: str, full_name: str
    ):
        sent["admin_email"] = admin_email
        sent["activation_url"] = activation_url
        sent["user_email"] = user_email
        sent["full_name"] = full_name
        return True

    monkeypatch.setattr(
        "src.api.v1.router_users.send_user_activation_email",
        fake_send_user_activation_email,
    )

    payload = {
        "email": "newuser@example.com",
        "password": "password123",
        "full_name": "New User",
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 201
    assert sent["admin_email"] == (
        settings.ADMIN_NOTIFICATION_EMAIL or settings.DEFAULT_ADMIN_EMAIL
    )
    token = sent["activation_url"].split("token=")[-1]
    decoded = security.verify_activation_token(token)
    assert decoded is not None


def test_activate_user_with_token(client: TestClient, db_session: Session):
    user_in = user_schema.UserCreate(
        email="activate_me@example.com",
        password="password",
        full_name="Activate Me",
    )
    user = crud_user.create_user(db_session, user=user_in)
    token = security.create_activation_token(str(user.id))

    response = client.get(f"/users/activate?token={token}")
    assert response.status_code == 200
    db_session.refresh(user)
    assert user.is_active is True
