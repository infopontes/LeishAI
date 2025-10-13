from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from .test_utils import get_authenticated_headers


def test_create_animal(client: TestClient, db_session: Session):
    """
    Testa a criação de um novo animal por um usuário autenticado.
    """
    # 1. Obter cabeçalhos de autenticação
    headers = get_authenticated_headers(client, db_session, "vet@example.com")

    # 2. Pré-requisito: Criar um Proprietário (Owner) via API
    owner_data = {"name": "José Bezerra", "city": "Parnaíba"}
    response_owner = client.post("/owners/", headers=headers, json=owner_data)
    assert response_owner.status_code == 201
    owner_id = response_owner.json()["id"]

    # --- INÍCIO DA CORREÇÃO ---
    # 3. Pré-requisito: Criar uma Raça (Breed) via API
    #    Para isso, precisamos de um usuário admin.

    admin_headers = get_authenticated_headers(
        client, db_session, "admin@dsleish.com", role_name="admin"
    )

    breed_data = {"name": "Poodle de Teste"}
    response_breed = client.post(
        "/breeds/", headers=admin_headers, json=breed_data
    )
    assert response_breed.status_code == 201
    breed_id = response_breed.json()["id"]
    # --- FIM DA CORREÇÃO ---

    # 4. Dados do novo animal
    animal_data = {
        "name": "Rex",
        "sex": "M",
        "original_id": "A123",
        "owner_id": owner_id,
        "breed_id": breed_id,
    }

    # 5. Fazer a requisição POST para o endpoint que queremos criar
    response = client.post("/animals/", headers=headers, json=animal_data)

    # 6. Asserções
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["name"] == animal_data["name"]
    assert data["owner"]["id"] == owner_id
    assert data["breed"]["id"] == breed_id


def test_create_animal_unauthorized(client: TestClient):
    """
    Testa que um usuário não autenticado não pode criar um animal.
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
    Testa a listagem de animais por um usuário autenticado.
    """
    # 1. Obter cabeçalhos de autenticação e criar os pré-requisitos (owner, breed)
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

    # 2. Criar um animal para garantir que a lista não esteja vazia
    animal_data = {
        "name": "Bolinha",
        "owner_id": owner_id,
        "breed_id": breed_id,
    }
    response_create = client.post(
        "/animals/", headers=headers, json=animal_data
    )
    assert response_create.status_code == 201

    # 3. Fazer a requisição GET para listar os animais
    response_read = client.get("/animals/", headers=headers)

    # 4. Asserções
    assert response_read.status_code == 200, response_read.text
    data = response_read.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Verifica se o nome do animal criado está na lista retornada
    assert any(animal["name"] == animal_data["name"] for animal in data)
