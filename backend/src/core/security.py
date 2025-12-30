from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt
from passlib.context import CryptContext

from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Checks if the provided password matches the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generates a hash of a password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Creates a new access token (JWT).
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # If no expiration time is provided, sets a default of 15 minutes
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    # Adds expiration time to token payload
    to_encode.update({"exp": expire})

    # Encrypts the token using the secret key and algorithm defined in the settings
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_password_reset_token(email: str) -> str:
    expires = timedelta(
        minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES
    )
    return create_access_token(
        data={"sub": email, "scope": "password_reset"},
        expires_delta=expires,
    )


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if payload.get("scope") != "password_reset":
            return None
        return payload.get("sub")
    except Exception:
        return None


def create_activation_token(user_id: str) -> str:
    expires = timedelta(minutes=60 * 24)  # 24 hours
    return create_access_token(
        data={"sub": user_id, "scope": "activate_user"},
        expires_delta=expires,
    )


def verify_activation_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        if payload.get("scope") != "activate_user":
            return None
        return payload.get("sub")
    except Exception:
        return None
