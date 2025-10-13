from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# A importação agora funciona por causa do __init__.py
from .test_utils import get_authenticated_headers


# As fixtures 'client' e 'db_session' agora são fornecidas automaticamente pelo conftest.py
def test_create_owner(client: TestClient, db_session: Session):
    """
    Testa a criação de um novo proprietário por um usuário autenticado.
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
    Testa que um usuário não autenticado não pode criar um proprietário.
    """
    owner_data = {"name": "Jane Doe"}
    response = client.post("/owners/", json=owner_data)

    assert response.status_code == 401, response.text


def test_read_owners(client: TestClient, db_session: Session):
    """
    Testa a listagem de proprietários por um usuário autenticado.
    """
    # 1. Criar um proprietário para garantir que a lista não esteja vazia
    owner_data = {"name": "Maria Oliveira", "city": "Teresina"}
    headers = get_authenticated_headers(
        client, db_session, "user2@example.com"
    )
    response_create = client.post("/owners/", headers=headers, json=owner_data)
    assert response_create.status_code == 201

    # 2. Fazer a requisição GET para listar os proprietários
    response_read = client.get("/owners/", headers=headers)

    # 3. Asserções
    assert response_read.status_code == 200, response_read.text
    data = response_read.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Verifica se o nome do proprietário criado está na lista retornada
    assert any(owner["name"] == owner_data["name"] for owner in data)


# ... (imports e testes existentes) ...


def test_read_owner_by_id(client: TestClient, db_session: Session):
    """
    Testa a busca de um proprietário específico pelo seu ID.
    """
    # 1. Criar um proprietário para ter um ID para buscar
    owner_data = {"name": "Ana Clara", "city": "Parnaíba"}
    headers = get_authenticated_headers(
        client, db_session, "user_for_get@example.com"
    )

    response_create = client.post("/owners/", headers=headers, json=owner_data)
    assert response_create.status_code == 201
    created_owner_id = response_create.json()["id"]

    # 2. Fazer a requisição GET para o endpoint que queremos criar
    response_read = client.get(f"/owners/{created_owner_id}", headers=headers)

    # 3. Asserções
    assert response_read.status_code == 200, response_read.text
    data = response_read.json()
    assert data["id"] == created_owner_id
    assert data["name"] == owner_data["name"]


def test_read_owner_by_id_not_found(client: TestClient, db_session: Session):
    """
    Testa que um erro 404 é retornado ao buscar um ID de proprietário inexistente.
    """
    # Usamos um UUID aleatório que certamente não existe
    non_existent_id = "123e4567-e89b-12d3-a456-426614174000"
    headers = get_authenticated_headers(
        client, db_session, "another_user@example.com"
    )

    response = client.get(f"/owners/{non_existent_id}", headers=headers)

    assert response.status_code == 404


# ... (imports e testes existentes) ...


def test_update_owner(client: TestClient, db_session: Session):
    """
    Testa a atualização dos dados de um proprietário existente.
    """
    # 1. Criar um proprietário para ter um ID para atualizar
    owner_data = {"name": "Ricardo Alves", "phone": "111111111"}
    headers = get_authenticated_headers(
        client, db_session, "user_for_update@example.com"
    )

    response_create = client.post("/owners/", headers=headers, json=owner_data)
    assert response_create.status_code == 201
    created_owner_id = response_create.json()["id"]

    # 2. Dados para a atualização
    updated_data = {"name": "Ricardo Alves da Silva", "phone": "86988887777"}

    # 3. Fazer a requisição PUT para o endpoint que queremos criar
    response_update = client.put(
        f"/owners/{created_owner_id}", headers=headers, json=updated_data
    )

    # 4. Asserções
    assert response_update.status_code == 200, response_update.text
    data = response_update.json()
    assert data["name"] == updated_data["name"]
    assert data["phone"] == updated_data["phone"]
    assert data["id"] == created_owner_id


def test_delete_owner(client: TestClient, db_session: Session):
    """
    Testa a remoção de um proprietário existente.
    """
    # 1. Criar um proprietário para ter um ID para apagar
    owner_data = {"name": "Usuario a ser Deletado"}
    headers = get_authenticated_headers(
        client, db_session, "user_for_delete@example.com"
    )

    response_create = client.post("/owners/", headers=headers, json=owner_data)
    assert response_create.status_code == 201
    created_owner_id = response_create.json()["id"]

    # 2. Fazer a requisição DELETE para o endpoint
    response_delete = client.delete(
        f"/owners/{created_owner_id}", headers=headers
    )

    # 3. Asserção para a resposta do DELETE
    assert response_delete.status_code == 204

    # 4. Verificar se o proprietário foi realmente apagado
    response_get = client.get(f"/owners/{created_owner_id}", headers=headers)
    assert response_get.status_code == 404
