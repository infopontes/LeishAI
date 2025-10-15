from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from .test_utils import get_authenticated_headers


def test_create_and_read_breed_by_id(client: TestClient, db_session: Session):
    """
    Tests the creation and search of a specific breed by its ID.
    """
    # 1. Use an admin user to create a race
    admin_headers = get_authenticated_headers(
        client, db_session, "admin_breed_test@example.com", role_name="admin"
    )
    breed_data = {"name": "Buldogue Francês"}

    response_create = client.post(
        "/breeds/", headers=admin_headers, json=breed_data
    )
    assert response_create.status_code == 201
    created_breed_id = response_create.json()["id"]

    # 2. Use a regular user to search for the breed (any logged in user can read)
    user_headers = get_authenticated_headers(
        client, db_session, "user_breed_test@example.com"
    )

    # 3. Make a GET request to the endpoint we want to create
    response_read = client.get(
        f"/breeds/{created_breed_id}", headers=user_headers
    )

    # 4. Assertions
    assert response_read.status_code == 200, response_read.text
    data = response_read.json()
    assert data["id"] == created_breed_id
    assert data["name"] == breed_data["name"]


def test_read_breed_by_id_not_found(client: TestClient, db_session: Session):
    """
    Tests that a 404 error is returned when fetching a non-existent breed ID.
    """
    non_existent_id = "123e4567-e89b-12d3-a456-426614174000"
    headers = get_authenticated_headers(
        client, db_session, "another_user_breed@example.com"
    )

    response = client.get(f"/breeds/{non_existent_id}", headers=headers)

    assert response.status_code == 404


def test_update_breed(client: TestClient, db_session: Session):
    """
    Tests updating the name of an existing race.
    """
    # 1. Use an admin user to create the breed
    admin_headers = get_authenticated_headers(
        client, db_session, "admin_for_update@example.com", role_name="admin"
    )
    breed_data = {"name": "Buldogue"}

    response_create = client.post(
        "/breeds/", headers=admin_headers, json=breed_data
    )
    assert response_create.status_code == 201
    created_breed_id = response_create.json()["id"]

    # 2. Data for the update
    updated_data = {"name": "Buldogue Inglês"}

    # 3. Make the PUT request to the endpoint we want to create
    response_update = client.put(
        f"/breeds/{created_breed_id}", headers=admin_headers, json=updated_data
    )

    # 4. Assertions
    assert response_update.status_code == 200, response_update.text
    data = response_update.json()
    assert data["name"] == updated_data["name"]
    assert data["id"] == created_breed_id


def test_delete_breed(client: TestClient, db_session: Session):
    """
    Tests the removal of an existing race.
    """
    # 1. Create a race to have an ID to delete
    admin_headers = get_authenticated_headers(
        client, db_session, "admin_for_delete@example.com", role_name="admin"
    )
    breed_data = {"name": "Raça a ser Deletada"}

    response_create = client.post(
        "/breeds/", headers=admin_headers, json=breed_data
    )
    assert response_create.status_code == 201
    created_breed_id = response_create.json()["id"]

    # 2. Make the DELETE request to the endpoint
    response_delete = client.delete(
        f"/breeds/{created_breed_id}", headers=admin_headers
    )

    # 3. Assertion for the DELETE response
    assert response_delete.status_code == 204

    # 4. Check if the race was actually deleted
    response_get = client.get(
        f"/breeds/{created_breed_id}", headers=admin_headers
    )
    assert response_get.status_code == 404
