from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from src.core.config import settings
from src.db import models

from src.db import crud
from src.db.database import SessionLocal
from src.schemas import user as user_schema

# Esta linha cria um "esquema" de segurança.
# O FastAPI saberá que, para se autenticar, o cliente precisa ir ao endpoint "/token".
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

router = APIRouter(prefix="/users", tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """
    Dependência para decodificar o token, validar o usuário e retorná-lo.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica o token JWT
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        # Extrai o email do campo "sub" (subject) do token
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        # Se o token for inválido ou expirar, levanta o erro
        raise credentials_exception

    # Busca o usuário no banco de dados
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        # Se o usuário não existir mais, levanta o erro
        raise credentials_exception

    # Retorna o objeto do usuário
    return user


# O endpoint de criação de usuário continua como antes, pois é público
@router.post(
    "/",
    response_model=user_schema.UserPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_new_user(
    user: user_schema.UserCreate, db: Session = Depends(get_db)
):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return crud.create_user(db=db, user=user)


@router.get("/me", response_model=user_schema.UserPublic)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    """
    Retorna os dados do usuário atualmente logado.
    A autenticação é gerenciada pela dependência 'get_current_user'.
    """
    return current_user
