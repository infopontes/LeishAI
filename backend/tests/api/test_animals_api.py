from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from .test_utils import get_authenticated_headers


def test_create_animal(client: TestClient, db_session: Session):
    """
    Tests the creation of a new animal by an authenticated user.
    """
    # 1. Get authentication headers
    headers = get_authenticated_headers(client, db_session, "vet@example.com")

    # 2. Prerequisite: Create an Owner via API
    owner_data = {"name": "José Bezerra", "city": "Parnaíba"}
    response_owner = client.post("/owners/", headers=headers, json=owner_data)
    assert response_owner.status_code == 201
    owner_id = response_owner.json()["id"]

    # 3. Prerequisite: Create a Breed via API
    # To do this, we need an admin user.

    admin_headers = get_authenticated_headers(
        client, db_session, "admin@dsleish.com", role_name="admin"
    )

    breed_data = {"name": "Poodle de Teste"}
    response_breed = client.post(
        "/breeds/", headers=admin_headers, json=breed_data
    )
    assert response_breed.status_code == 201
    breed_id = response_breed.json()["id"]

    # 4. New animal data
    animal_data = {
        "name": "Rex",
        "sex": "M",
        "original_id": "A123",
        "owner_id": owner_id,
        "breed_id": breed_id,
    }

    # 5. Make the POST request to the endpoint we want to create
    response = client.post("/animals/", headers=headers, json=animal_data)

    # 6. Assertions
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["name"] == animal_data["name"]
    assert data["owner"]["id"] == owner_id
    assert data["breed"]["id"] == breed_id


def test_create_animal_unauthorized(client: TestClient):
    """
    Tests that an unauthenticated user cannot create an animal.
    """
    animal_data = {
        "name": "Fido",
        "owner_id": "c6f7c8d9...",
        "breed_id": "c6f7c8d9...",
    }
    response = client.post("/animals/", json=animal_data)
    assert response.status_code == 401


def test_read_animals(client: TestClient, db_session: Session):
    """
    Tests the listing of animals by an authenticated user.
    """
    # 1. Get authentication headers and create prerequisites (owner, breed)
    headers = get_authenticated_headers(client, db_session, "vet2@example.com")
    admin_headers = get_authenticated_headers(
        client, db_session, "admin2@example.com", role_name="admin"
    )

    owner_data = {"name": "Ana Sousa"}
    response_owner = client.post("/owners/", headers=headers, json=owner_data)
    owner_id = response_owner.json()["id"]

    breed_data = {"name": "Golden Retriever"}
    response_breed = client.post(
        "/breeds/", headers=admin_headers, json=breed_data
    )

    assert response_breed.status_code == 201, response_breed.text

    breed_id = response_breed.json()["id"]

    # 2. Create an animal to ensure the list is not empty
    animal_data = {
        "name": "Bolinha",
        "owner_id": owner_id,
        "breed_id": breed_id,
    }
    response_create = client.post(
        "/animals/", headers=headers, json=animal_data
    )
    assert response_create.status_code == 201

    # 3. Make a GET request to list the animals
    response_read = client.get("/animals/", headers=headers)

    # 4. Assertions
    assert response_read.status_code == 200, response_read.text
    data = response_read.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Checks if the name of the created animal is in the returned list
    assert any(animal["name"] == animal_data["name"] for animal in data)


def test_read_animal_by_id(client: TestClient, db_session: Session):
    """
    Testa a busca de um animal específico pelo seu ID.
    """
    # 1. Create all prerequisites: owner, breed, and animal
    vet_headers = get_authenticated_headers(
        client, db_session, "vet_get_animal@example.com"
    )
    admin_headers = get_authenticated_headers(
        client, db_session, "admin_get_animal@example.com", role_name="admin"
    )

    owner_data = {"name": "Mariana Costa"}
    response_owner = client.post(
        "/owners/", headers=vet_headers, json=owner_data
    )
    owner_id = response_owner.json()["id"]

    breed_data = {"name": "Golden Doodle"}
    response_breed = client.post(
        "/breeds/", headers=admin_headers, json=breed_data
    )
    breed_id = response_breed.json()["id"]

    animal_data = {"name": "Max", "owner_id": owner_id, "breed_id": breed_id}
    response_create = client.post(
        "/animals/", headers=vet_headers, json=animal_data
    )
    assert response_create.status_code == 201
    created_animal_id = response_create.json()["id"]

    # 2. Make a GET request to the endpoint we want to create
    response_read = client.get(
        f"/animals/{created_animal_id}", headers=vet_headers
    )

    # 3. Assertions
    assert response_read.status_code == 200, response_read.text
    data = response_read.json()
    assert data["id"] == created_animal_id
    assert data["name"] == animal_data["name"]


def test_read_animal_by_id_not_found(client: TestClient, db_session: Session):
    """
    Tests that a 404 error is returned when fetching a non-existent animal ID.
    """
    non_existent_id = "123e4567-e89b-12d3-a456-426614174000"
    headers = get_authenticated_headers(
        client, db_session, "another_user_animal@example.com"
    )

    response = client.get(f"/animals/{non_existent_id}", headers=headers)

    assert response.status_code == 404


def test_update_animal(client: TestClient, db_session: Session):
    """
    Tests updating data for an existing animal.
    """
    # 1. Create all prerequisites
    vet_headers = get_authenticated_headers(
        client, db_session, "vet_update_animal@example.com"
    )
    admin_headers = get_authenticated_headers(
        client,
        db_session,
        "admin_update_animal@example.com",
        role_name="admin",
    )

    owner_data = {"name": "Mariana Costa"}
    response_owner = client.post(
        "/owners/", headers=vet_headers, json=owner_data
    )
    owner_id = response_owner.json()["id"]

    breed_data = {"name": "Golden Doodle"}
    response_breed = client.post(
        "/breeds/", headers=admin_headers, json=breed_data
    )
    breed_id = response_breed.json()["id"]

    animal_data = {
        "name": "Max",
        "sex": "M",
        "owner_id": owner_id,
        "breed_id": breed_id,
    }
    response_create = client.post(
        "/animals/", headers=vet_headers, json=animal_data
    )
    assert response_create.status_code == 201
    created_animal_id = response_create.json()["id"]

    # 2. Data for update (it is not necessary to send all fields)
    updated_data = {"name": "Maximus", "sex": "M"}

    # 3. Make the PUT request to the endpoint we want to create
    response_update = client.put(
        f"/animals/{created_animal_id}", headers=vet_headers, json=updated_data
    )

    # 4. Assertions
    assert response_update.status_code == 200, response_update.text
    data = response_update.json()
    assert data["name"] == updated_data["name"]
    assert data["sex"] == updated_data["sex"]
    assert data["id"] == created_animal_id


def test_delete_animal(client: TestClient, db_session: Session):
    """
    Testa a remoção de um animal existente.
    """
    # 1. Create all prerequisites
    vet_headers = get_authenticated_headers(
        client, db_session, "vet_delete_animal@example.com"
    )
    admin_headers = get_authenticated_headers(
        client,
        db_session,
        "admin_delete_animal@example.com",
        role_name="admin",
    )

    owner_data = {"name": "Usuario a ser Deletado"}
    response_owner = client.post(
        "/owners/", headers=vet_headers, json=owner_data
    )
    owner_id = response_owner.json()["id"]

    breed_data = {"name": "Raça a ser Deletada"}
    response_breed = client.post(
        "/breeds/", headers=admin_headers, json=breed_data
    )
    breed_id = response_breed.json()["id"]

    animal_data = {
        "name": "Animal a ser Deletado",
        "owner_id": owner_id,
        "breed_id": breed_id,
    }
    response_create = client.post(
        "/animals/", headers=vet_headers, json=animal_data
    )
    assert response_create.status_code == 201
    created_animal_id = response_create.json()["id"]

    # 2. Make the DELETE request to the endpoint
    response_delete = client.delete(
        f"/animals/{created_animal_id}", headers=vet_headers
    )

    # 3. Assertion for the DELETE response
    assert response_delete.status_code == 204

    # 4. Check if the animal was actually deleted
    response_get = client.get(
        f"/animals/{created_animal_id}", headers=vet_headers
    )
    assert response_get.status_code == 404
