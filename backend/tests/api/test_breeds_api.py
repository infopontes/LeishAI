from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from .test_utils import get_authenticated_headers


def test_create_and_read_breed_by_id(client: TestClient, db_session: Session):
    """
    Testa a criação e a busca de uma raça específica pelo seu ID.
    """
    # 1. Utilizar um utilizador admin para criar uma raça
    admin_headers = get_authenticated_headers(
        client, db_session, "admin_breed_test@example.com", role_name="admin"
    )
    breed_data = {"name": "Buldogue Francês"}

    response_create = client.post(
        "/breeds/", headers=admin_headers, json=breed_data
    )
    assert response_create.status_code == 201
    created_breed_id = response_create.json()["id"]

    # 2. Utilizar um utilizador comum para buscar a raça (qualquer utilizador logado pode ler)
    user_headers = get_authenticated_headers(
        client, db_session, "user_breed_test@example.com"
    )

    # 3. Fazer a requisição GET para o endpoint que queremos criar
    response_read = client.get(
        f"/breeds/{created_breed_id}", headers=user_headers
    )

    # 4. Asserções
    assert response_read.status_code == 200, response_read.text
    data = response_read.json()
    assert data["id"] == created_breed_id
    assert data["name"] == breed_data["name"]


def test_read_breed_by_id_not_found(client: TestClient, db_session: Session):
    """
    Testa que um erro 404 é retornado ao buscar um ID de raça inexistente.
    """
    non_existent_id = "123e4567-e89b-12d3-a456-426614174000"
    headers = get_authenticated_headers(
        client, db_session, "another_user_breed@example.com"
    )

    response = client.get(f"/breeds/{non_existent_id}", headers=headers)

    assert response.status_code == 404


def test_update_breed(client: TestClient, db_session: Session):
    """
    Testa a atualização do nome de uma raça existente.
    """
    # 1. Utilizar um utilizador admin para criar a raça
    admin_headers = get_authenticated_headers(
        client, db_session, "admin_for_update@example.com", role_name="admin"
    )
    breed_data = {"name": "Buldogue"}

    response_create = client.post(
        "/breeds/", headers=admin_headers, json=breed_data
    )
    assert response_create.status_code == 201
    created_breed_id = response_create.json()["id"]

    # 2. Dados para a atualização
    updated_data = {"name": "Buldogue Inglês"}

    # 3. Fazer a requisição PUT para o endpoint que queremos criar
    response_update = client.put(
        f"/breeds/{created_breed_id}", headers=admin_headers, json=updated_data
    )

    # 4. Asserções
    assert response_update.status_code == 200, response_update.text
    data = response_update.json()
    assert data["name"] == updated_data["name"]
    assert data["id"] == created_breed_id


def test_delete_breed(client: TestClient, db_session: Session):
    """
    Testa a remoção de uma raça existente.
    """
    # 1. Criar uma raça para ter um ID para apagar
    admin_headers = get_authenticated_headers(
        client, db_session, "admin_for_delete@example.com", role_name="admin"
    )
    breed_data = {"name": "Raça a ser Deletada"}

    response_create = client.post(
        "/breeds/", headers=admin_headers, json=breed_data
    )
    assert response_create.status_code == 201
    created_breed_id = response_create.json()["id"]

    # 2. Fazer a requisição DELETE para o endpoint
    response_delete = client.delete(
        f"/breeds/{created_breed_id}", headers=admin_headers
    )

    # 3. Asserção para a resposta do DELETE
    assert response_delete.status_code == 204

    # 4. Verificar se a raça foi realmente apagada
    response_get = client.get(
        f"/breeds/{created_breed_id}", headers=admin_headers
    )
    assert response_get.status_code == 404
