from src.db.crud import crud_user
from src.schemas.user import UserCreate


def test_create_and_retrieve_user(
    db_session,
):  # db_session agora vem do conftest.py
    """
    Testa a criação e a busca de um usuário no banco de dados.
    """
    user_email = "test@example.com"
    user_password = "testpassword123"

    user_in = UserCreate(email=user_email, password=user_password)
    db_user = crud_user.create_user(db=db_session, user=user_in)

    assert db_user.email == user_email
    assert db_user.role is not None
    assert db_user.role.name == "veterinario"

    retrieved_user = crud_user.get_user_by_email(
        db=db_session, email=user_email
    )

    assert retrieved_user
    assert retrieved_user.email == user_email
    assert retrieved_user.id == db_user.id
