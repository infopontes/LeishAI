from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .test_utils import get_authenticated_headers
from src.db.models import enums  # Precisamos dos nossos Enums


def test_create_assessment(client: TestClient, db_session: Session):
    """
    Testa a criação de um novo atendimento por um usuário autenticado.
    """
    # 1. Obter cabeçalhos de autenticação para um veterinário
    vet_headers = get_authenticated_headers(
        client, db_session, "vet3@example.com"
    )

    # 2. Pré-requisito: Criar um Proprietário e uma Raça
    admin_headers = get_authenticated_headers(
        client, db_session, "admin3@example.com", role_name="admin"
    )
    owner_data = {"name": "Carlos Pereira"}
    response_owner = client.post(
        "/owners/", headers=vet_headers, json=owner_data
    )
    owner_id = response_owner.json()["id"]

    breed_data = {"name": "Beagle"}
    response_breed = client.post(
        "/breeds/", headers=admin_headers, json=breed_data
    )
    breed_id = response_breed.json()["id"]

    # 3. Pré-requisito: Criar um Animal
    animal_data = {
        "name": "Snoopy",
        "owner_id": owner_id,
        "breed_id": breed_id,
    }
    response_animal = client.post(
        "/animals/", headers=vet_headers, json=animal_data
    )
    assert response_animal.status_code == 201
    animal_id = response_animal.json()["id"]

    # 4. Dados do novo atendimento
    assessment_data = {
        "animal_id": animal_id,
        "general_state": enums.GeneralState.bom,
        "nutritional_state": enums.NutritionalState.adequado,
        "ectoparasites": enums.Severity.ausente,
        "diagnosis": enums.DiagnosisResult.negativo,
    }

    # 5. Fazer a requisição POST para o endpoint que queremos criar
    response = client.post(
        "/assessments/", headers=vet_headers, json=assessment_data
    )

    # 6. Asserções: O que esperamos que aconteça
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["general_state"] == assessment_data["general_state"]
    assert data["diagnosis"] == assessment_data["diagnosis"]
    assert "id" in data
    # Verifica se os objetos aninhados foram retornados corretamente
    assert data["animal"]["id"] == animal_id
    # O 'user' associado deve ser o veterinário que fez a requisição
    user_making_request = client.get("/users/me", headers=vet_headers).json()
    assert data["user"]["id"] == user_making_request["id"]


def test_read_assessments(client: TestClient, db_session: Session):
    """
    Testa a listagem de atendimentos por um usuário autenticado.
    """
    # 1. Preparar o ambiente: criar owner, breed, e animal
    vet_headers = get_authenticated_headers(
        client, db_session, "vet4@example.com"
    )
    admin_headers = get_authenticated_headers(
        client, db_session, "admin4@example.com", role_name="admin"
    )

    owner_data = {"name": "Fernanda Lima"}
    response_owner = client.post(
        "/owners/", headers=vet_headers, json=owner_data
    )
    owner_id = response_owner.json()["id"]

    breed_data = {"name": "Shih Tzu"}
    response_breed = client.post(
        "/breeds/", headers=admin_headers, json=breed_data
    )
    breed_id = response_breed.json()["id"]

    animal_data = {"name": "Lili", "owner_id": owner_id, "breed_id": breed_id}
    response_animal = client.post(
        "/animals/", headers=vet_headers, json=animal_data
    )
    animal_id = response_animal.json()["id"]

    # 2. Criar um atendimento para garantir que a lista não esteja vazia
    assessment_data = {
        "animal_id": animal_id,
        "diagnosis": enums.DiagnosisResult.negativo,
    }
    response_create = client.post(
        "/assessments/", headers=vet_headers, json=assessment_data
    )
    assert response_create.status_code == 201
    created_assessment_id = response_create.json()["id"]

    # 3. Fazer a requisição GET para listar os atendimentos
    response_read = client.get("/assessments/", headers=vet_headers)

    # 4. Asserções
    assert response_read.status_code == 200, response_read.text
    data = response_read.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Verifica se o ID do atendimento criado está na lista retornada
    assert any(
        assessment["id"] == created_assessment_id for assessment in data
    )


# ... (imports e testes existentes) ...


def test_read_assessment_by_id(client: TestClient, db_session: Session):
    """
    Testa a busca de um atendimento específico pelo seu ID.
    """
    # 1. Criar todos os pré-requisitos
    vet_headers = get_authenticated_headers(
        client, db_session, "vet_get_assessment@example.com"
    )
    admin_headers = get_authenticated_headers(
        client,
        db_session,
        "admin_get_assessment@example.com",
        role_name="admin",
    )

    owner_data = {"name": "Juliana Paes"}
    response_owner = client.post(
        "/owners/", headers=vet_headers, json=owner_data
    )
    owner_id = response_owner.json()["id"]

    breed_data = {"name": "Spitz Alemão"}
    response_breed = client.post(
        "/breeds/", headers=admin_headers, json=breed_data
    )
    breed_id = response_breed.json()["id"]

    animal_data = {"name": "Lulu", "owner_id": owner_id, "breed_id": breed_id}
    response_animal = client.post(
        "/animals/", headers=vet_headers, json=animal_data
    )
    animal_id = response_animal.json()["id"]

    assessment_data = {
        "animal_id": animal_id,
        "diagnosis": enums.DiagnosisResult.negativo,
    }
    response_create = client.post(
        "/assessments/", headers=vet_headers, json=assessment_data
    )
    assert response_create.status_code == 201
    created_assessment_id = response_create.json()["id"]

    # 2. Fazer a requisição GET para o endpoint que queremos criar
    response_read = client.get(
        f"/assessments/{created_assessment_id}", headers=vet_headers
    )

    # 3. Asserções
    assert response_read.status_code == 200, response_read.text
    data = response_read.json()
    assert data["id"] == created_assessment_id
    assert data["diagnosis"] == assessment_data["diagnosis"]


def test_read_assessment_by_id_not_found(
    client: TestClient, db_session: Session
):
    """
    Testa que um erro 404 é retornado ao buscar um ID de atendimento inexistente.
    """
    non_existent_id = "123e4567-e89b-12d3-a456-426614174000"
    headers = get_authenticated_headers(
        client, db_session, "another_user_assessment@example.com"
    )

    response = client.get(f"/assessments/{non_existent_id}", headers=headers)

    assert response.status_code == 404


def test_update_assessment(client: TestClient, db_session: Session):
    """
    Testa a atualização dos dados de um atendimento existente.
    """
    # 1. Criar todos os pré-requisitos
    vet_headers = get_authenticated_headers(
        client, db_session, "vet_update_assessment@example.com"
    )
    admin_headers = get_authenticated_headers(
        client,
        db_session,
        "admin_update_assessment@example.com",
        role_name="admin",
    )

    owner_data = {"name": "Ricardo Pereira"}
    response_owner = client.post(
        "/owners/", headers=vet_headers, json=owner_data
    )
    owner_id = response_owner.json()["id"]

    breed_data = {"name": "Rottweiler de Teste"}
    response_breed = client.post(
        "/breeds/", headers=admin_headers, json=breed_data
    )
    breed_id = response_breed.json()["id"]

    animal_data = {
        "name": "Brutus",
        "owner_id": owner_id,
        "breed_id": breed_id,
    }
    response_animal = client.post(
        "/animals/", headers=vet_headers, json=animal_data
    )
    animal_id = response_animal.json()["id"]

    assessment_data = {
        "animal_id": animal_id,
        "general_state": enums.GeneralState.bom,
        "diagnosis": enums.DiagnosisResult.negativo,
    }
    response_create = client.post(
        "/assessments/", headers=vet_headers, json=assessment_data
    )
    assert response_create.status_code == 201
    created_assessment_id = response_create.json()["id"]

    # 2. Dados para a atualização
    updated_data = {
        "general_state": enums.GeneralState.regular,
        "diagnosis": enums.DiagnosisResult.positivo,
    }

    # 3. Fazer a requisição PUT para o endpoint que queremos criar
    response_update = client.put(
        f"/assessments/{created_assessment_id}",
        headers=vet_headers,
        json=updated_data,
    )

    # 4. Asserções
    assert response_update.status_code == 200, response_update.text
    data = response_update.json()
    assert data["general_state"] == updated_data["general_state"]
    assert data["diagnosis"] == updated_data["diagnosis"]
    assert data["id"] == created_assessment_id


def test_delete_assessment(client: TestClient, db_session: Session):
    """
    Testa a remoção de um atendimento existente.
    """
    # 1. Criar todos os pré-requisitos
    vet_headers = get_authenticated_headers(
        client, db_session, "vet_delete_assessment@example.com"
    )
    admin_headers = get_authenticated_headers(
        client,
        db_session,
        "admin_delete_assessment@example.com",
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
    response_animal = client.post(
        "/animals/", headers=vet_headers, json=animal_data
    )
    animal_id = response_animal.json()["id"]

    assessment_data = {"animal_id": animal_id}
    response_create = client.post(
        "/assessments/", headers=vet_headers, json=assessment_data
    )
    assert response_create.status_code == 201
    created_assessment_id = response_create.json()["id"]

    # 2. Fazer a requisição DELETE para o endpoint
    response_delete = client.delete(
        f"/assessments/{created_assessment_id}", headers=vet_headers
    )

    # 3. Asserção para a resposta do DELETE
    assert response_delete.status_code == 204

    # 4. Verificar se o atendimento foi realmente apagado
    response_get = client.get(
        f"/assessments/{created_assessment_id}", headers=vet_headers
    )
    assert response_get.status_code == 404
