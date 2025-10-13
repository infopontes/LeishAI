from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from .test_utils import get_authenticated_headers


def test_read_users_as_admin(client: TestClient, db_session: Session):
    """
    Testa a listagem de todos os usuários por um usuário administrador.
    """
    # Cria um usuário comum para garantir que a lista não esteja vazia
    get_authenticated_headers(client, db_session, "common_user@example.com")

    # Obtém cabeçalhos para um usuário admin
    admin_headers = get_authenticated_headers(
        client, db_session, "admin_for_test@example.com", role_name="admin"
    )

    # Faz a requisição para o endpoint que queremos criar
    response = client.get("/users/", headers=admin_headers)

    # Asserções
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # Deve haver pelo menos o admin e o usuário comum


def test_read_users_as_non_admin_fails(
    client: TestClient, db_session: Session
):
    """
    Testa que um usuário não-administrador não pode listar todos os usuários.
    """
    # Obtém cabeçalhos para um usuário com perfil 'veterinario'
    vet_headers = get_authenticated_headers(
        client, db_session, "vet_for_test@example.com", role_name="veterinario"
    )

    # Faz a requisição para o mesmo endpoint
    response = client.get("/users/", headers=vet_headers)

    # Asserção: Esperamos um erro 403 Forbidden
    assert response.status_code == 403, response.text
    assert (
        response.json()["detail"] == "The user does not have enough privileges"
    )
