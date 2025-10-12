from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from src.schemas.user import UserCreate
from src.db.crud import crud_user


def get_authenticated_headers(
    client: TestClient, db: Session, email: str
) -> dict[str, str]:
    """
    Cria um usuário (se não existir), faz login e retorna os cabeçalhos de autorização.
    """
    password = "testpassword"
    user = crud_user.get_user_by_email(db, email=email)
    if not user:
        user_in = UserCreate(email=email, password=password)
        crud_user.create_user(db, user=user_in)

    login_data = {"username": email, "password": password}
    response = client.post("/token", data=login_data)
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    return headers
