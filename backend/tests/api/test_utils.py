from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from typing import Optional

from src.schemas.user import UserCreate
from src.schemas.role import RoleCreate
from src.db.crud import crud_user, crud_role


def get_authenticated_headers(
    client: TestClient,
    db: Session,
    email: str,
    role_name: Optional[str] = None,
) -> dict[str, str]:
    """
    Cria um utilizador (se não existir), garante que está ativo,
    faz login e retorna os cabeçalhos de autorização.
    """
    password = "testpassword"
    user = crud_user.get_user_by_email(db, email=email)

    if not user:
        user_in = UserCreate(
            email=email, password=password, full_name=f"Test User {email}"
        )
        user = crud_user.create_user(db, user=user_in)

        # --- INÍCIO DA CORREÇÃO ---
        # Garante que o utilizador criado para o teste está ativo
        user.is_active = True
        # --- FIM DA CORREÇÃO ---

        if role_name:
            role = crud_role.get_role_by_name(db, name=role_name)
            if not role:
                role_in = RoleCreate(
                    name=role_name, description=f"Test {role_name}"
                )
                role = crud_role.create_role(db, role=role_in)

            user.role_id = role.id

        db.commit()
        db.refresh(user)

    login_data = {"username": email, "password": password}
    response = client.post("/token", data=login_data)

    # Adicionamos uma verificação para dar um erro mais claro se o login falhar
    if response.status_code != 200:
        raise Exception(
            f"Failed to log in user {email}. Response: {response.text}"
        )

    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    return headers
