from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core import security
from src.core.config import settings
from src.db import crud

# Vamos reutilizar a função get_db que já existe no router de usuários
from src.api.v1.router_users import get_db

router = APIRouter(tags=["Authentication"])


@router.post("/token")
def login_for_access_token(
    db: Session = Depends(get_db),
    # O FastAPI usa esta dependência para pegar 'username' e 'password' de um form-data
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Recebe as credenciais (email e senha) e retorna um token JWT.
    """
    # 1. Autentica o usuário (verificaremos a senha aqui)
    # Nota: OAuth2PasswordRequestForm chama o campo de login de 'username' por padrão.
    user = crud.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        # Se o usuário não for encontrado ou a senha estiver errada, levanta um erro 401.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2. Se a autenticação for bem-sucedida, cria o token de acesso
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    # 3. Retorna o token para o cliente
    return {"access_token": access_token, "token_type": "bearer"}
