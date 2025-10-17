# tests/api/test_prediction_api.py

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from .test_utils import get_authenticated_headers


def test_make_prediction(client: TestClient, db_session: Session):
    """
    Tests making a prediction with valid clinical data.
    """
    vet_headers = get_authenticated_headers(
        client, db_session, "vet_for_prediction@example.com"
    )

    prediction_data = {
        "general_state": "Bom",
        "ectoparasites": "Leve",
        "nutritional_state": "Leve a Moderado",
        "coat": "Leves/Moderadas",
        "nails": "Normal",
        "mucosa_color": "Normal (Rosa-claro)",
        "muzzle_ear_lesion": "Presente",
        "lymph_nodes": "Leves/Moderadas",
        "blepharitis": "Ausente",
        "conjunctivitis": "Ausente",
        "alopecia": "Presente",
        "bleeding": "Ausente",
        "skin_lesion": "Ausente",
        "muzzle_lip_depigmentation": "Ausente",
        "animal_sex": "M",
        "breed_name": "SRD",
    }

    response = client.post(
        "/predict/", headers=vet_headers, json=prediction_data
    )

    assert response.status_code == 200, response.text
    data = response.json()

    # --- UPDATED ASSERTIONS ---
    assert "diagnosis_prediction" in data
    assert "confidence_score" in data
    assert data["diagnosis_prediction"] in ["Positivo", "Negativo"]
    assert 0.0 <= data["confidence_score"] <= 1.0
