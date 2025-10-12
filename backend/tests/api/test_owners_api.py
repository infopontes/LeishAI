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
