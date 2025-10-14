from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from .test_utils import get_authenticated_headers
from src.schemas import user as user_schema
from src.db.crud import crud_user, crud_role
from src.schemas.role import RoleCreate


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


def test_update_user_as_admin(client: TestClient, db_session: Session):
    """
    Testa se um admin pode atualizar o nome e o perfil de outro utilizador.
    """
    # 1. Criar o utilizador admin e o utilizador alvo
    admin_headers = get_authenticated_headers(
        client, db_session, "admin_to_update@example.com", role_name="admin"
    )
    target_user_in = user_schema.UserCreate(
        email="target@example.com",
        password="password",
        full_name="Nome Antigo",
    )
    target_user = crud_user.create_user(db_session, user=target_user_in)

    # 2. Criar o novo perfil para o qual vamos mudar o utilizador
    new_role_in = RoleCreate(
        name="coordenador_teste", description="Perfil de Teste"
    )
    new_role = crud_role.create_role(db_session, role=new_role_in)

    # 3. Dados para a atualização
    update_data = {
        "full_name": "Nome Novo Atualizado",
        "institution": "Nova Instituição",
        "role_id": str(
            new_role.id
        ),  # Convertemos o UUID para string para o JSON
    }

    # 4. Fazer a requisição PUT
    response = client.put(
        f"/users/{target_user.id}", headers=admin_headers, json=update_data
    )

    # 5. Asserções
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["full_name"] == update_data["full_name"]
    assert data["institution"] == update_data["institution"]
    assert data["role"]["id"] == update_data["role_id"]


def test_update_user_as_non_admin_fails(
    client: TestClient, db_session: Session
):
    """
    Testa que um utilizador não-admin não pode atualizar outro utilizador.
    """
    # 1. Criar o utilizador não-admin e o utilizador alvo
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

    # 2. Dados de atualização (não devem ser aplicados)
    update_data = {"full_name": "Nome que não deve ser atualizado"}

    # 3. Fazer a requisição PUT
    response = client.put(
        f"/users/{target_user.id}", headers=vet_headers, json=update_data
    )

    # 4. Asserção
    assert response.status_code == 403


# ... (imports e outros testes) ...

def test_deactivate_user_as_admin(client: TestClient, db_session: Session):
    """
    Testa a desativação ('soft delete') de um utilizador por um administrador.
    """
    admin_headers = get_authenticated_headers(
        client, db_session, "admin_for_delete@example.com", role_name="admin"
    )
    target_user_in = user_schema.UserCreate(
        email="user_to_deactivate@example.com", password="password", full_name="Utilizador a Desativar"
    )
    target_user = crud_user.create_user(db_session, user=target_user_in)
    assert target_user.is_active is False # A asserção agora vai passar

    # Ativar o utilizador antes de o poder desativar
    target_user.is_active = True
    db_session.commit()
    db_session.refresh(target_user)
    assert target_user.is_active is True

    # Fazer a requisição DELETE
    response_delete = client.delete(f"/users/{target_user.id}", headers=admin_headers)

    assert response_delete.status_code == 204

    # Verificar se foi desativado
    db_session.refresh(target_user)
    assert target_user.is_active is False

    # Tentar fazer login e verificar se falha
    login_data = {"username": "user_to_deactivate@example.com", "password": "password"}
    response_login = client.post("/auth/token", data=login_data)
    assert response_login.status_code == 401