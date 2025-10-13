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


# ... (imports e testes existentes) ...


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
