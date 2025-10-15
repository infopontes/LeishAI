from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .test_utils import get_authenticated_headers


# The 'client' and 'db_session' fixtures are now automatically provided by conftest.py
def test_create_owner(client: TestClient, db_session: Session):
    """
    Tests the creation of a new owner by an authenticated user.
    """
    owner_data = {
        "name": "João da Silva",
        "phone": "86999998888",
        "city": "Parnaíba",
    }

    headers = get_authenticated_headers(client, db_session, "user@example.com")

    response = client.post("/owners/", headers=headers, json=owner_data)

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["name"] == owner_data["name"]
    assert data["phone"] == owner_data["phone"]
    assert "id" in data


def test_create_owner_unauthorized(client: TestClient):
    """
    Tests that an unauthenticated user cannot create an owner.
    """
    owner_data = {"name": "Jane Doe"}
    response = client.post("/owners/", json=owner_data)

    assert response.status_code == 401, response.text


def test_read_owners(client: TestClient, db_session: Session):
    """
    Tests the listing of owners by an authenticated user.
    """
    # 1. Create an owner to ensure the list is not empty
    owner_data = {"name": "Maria Oliveira", "city": "Teresina"}
    headers = get_authenticated_headers(
        client, db_session, "user2@example.com"
    )
    response_create = client.post("/owners/", headers=headers, json=owner_data)
    assert response_create.status_code == 201

    # 2. Make a GET request to list the owners
    response_read = client.get("/owners/", headers=headers)

    # 3. Assertions
    assert response_read.status_code == 200, response_read.text
    data = response_read.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Checks if the created owner name is in the returned list
    assert any(owner["name"] == owner_data["name"] for owner in data)


def test_read_owner_by_id(client: TestClient, db_session: Session):
    """
    Tests the search for a specific owner by their ID.
    """
    # 1. Create an owner to have an ID to search
    owner_data = {"name": "Ana Clara", "city": "Parnaíba"}
    headers = get_authenticated_headers(
        client, db_session, "user_for_get@example.com"
    )

    response_create = client.post("/owners/", headers=headers, json=owner_data)
    assert response_create.status_code == 201
    created_owner_id = response_create.json()["id"]

    # 2. Make a GET request to the endpoint we want to create
    response_read = client.get(f"/owners/{created_owner_id}", headers=headers)

    # 3. Assertions
    assert response_read.status_code == 200, response_read.text
    data = response_read.json()
    assert data["id"] == created_owner_id
    assert data["name"] == owner_data["name"]


def test_read_owner_by_id_not_found(client: TestClient, db_session: Session):
    """
    Testa que um erro 404 é retornado ao buscar um ID de proprietário inexistente.
    """
    # We use a random UUID that certainly doesn't exist
    non_existent_id = "123e4567-e89b-12d3-a456-426614174000"
    headers = get_authenticated_headers(
        client, db_session, "another_user@example.com"
    )

    response = client.get(f"/owners/{non_existent_id}", headers=headers)

    assert response.status_code == 404


def test_update_owner(client: TestClient, db_session: Session):
    """
    Tests updating data for an existing owner.
    """
    # 1. Create an owner to have an ID to update
    owner_data = {"name": "Ricardo Alves", "phone": "111111111"}
    headers = get_authenticated_headers(
        client, db_session, "user_for_update@example.com"
    )

    response_create = client.post("/owners/", headers=headers, json=owner_data)
    assert response_create.status_code == 201
    created_owner_id = response_create.json()["id"]

    # 2. Data for the update
    updated_data = {"name": "Ricardo Alves da Silva", "phone": "86988887777"}

    # 3. Make the PUT request to the endpoint we want to create
    response_update = client.put(
        f"/owners/{created_owner_id}", headers=headers, json=updated_data
    )

    # 4. Assertions
    assert response_update.status_code == 200, response_update.text
    data = response_update.json()
    assert data["name"] == updated_data["name"]
    assert data["phone"] == updated_data["phone"]
    assert data["id"] == created_owner_id


def test_delete_owner(client: TestClient, db_session: Session):
    """
    Tests the removal of an existing owner.
    """
    # 1. Create an owner to have an ID to delete
    owner_data = {"name": "Usuario a ser Deletado"}
    headers = get_authenticated_headers(
        client, db_session, "user_for_delete@example.com"
    )

    response_create = client.post("/owners/", headers=headers, json=owner_data)
    assert response_create.status_code == 201
    created_owner_id = response_create.json()["id"]

    # 2. Make the DELETE request to the endpoint
    response_delete = client.delete(
        f"/owners/{created_owner_id}", headers=headers
    )

    # 3. Assertion for the DELETE response
    assert response_delete.status_code == 204

    # 4. Check if the owner was actually deleted
    response_get = client.get(f"/owners/{created_owner_id}", headers=headers)
    assert response_get.status_code == 404
