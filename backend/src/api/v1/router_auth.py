from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.limiter import limiter
from src.core import security
from src.core.config import settings
from src.db.crud import crud_user
from src.schemas.auth import ForgotPasswordRequest, ResetPasswordRequest
from src.services.email import send_password_reset_email
from .dependencies import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])
PASSWORD_RESET_DETAIL = (
    "If the account exists, we've sent password reset instructions."
)


@router.post("/token")
@limiter.limit("100/minute")
def login_for_access_token(
    request: Request,
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Authenticates the user and generates a JWT access token.
    """
    user = crud_user.authenticate_user(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/forgot-password")
@limiter.limit("20/minute")
def forgot_password(
    request: Request,
    payload: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    """
    Starts the password reset flow without revealing if the email exists.
    """
    user = crud_user.get_user_by_email(db, email=payload.email)
    detail = PASSWORD_RESET_DETAIL
    if user and user.is_active:
        token = security.create_password_reset_token(user.email)
        reset_url = (
            f"{settings.FRONTEND_BASE_URL}/reset-password?token={token}"
        )
        email_sent = send_password_reset_email(
            to_email=user.email, reset_url=reset_url
        )
        if not email_sent:
            detail = "We couldn't send the reset email. Please try again later."

    return {"detail": detail}


@router.post("/reset-password")
@limiter.limit("20/minute")
def reset_password(
    request: Request,
    payload: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    """
    Resets the user's password using a valid reset token.
    """
    email = security.verify_password_reset_token(payload.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token"
        )

    user = crud_user.get_user_by_email(db, email=email)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user"
        )

    user.hashed_password = security.get_password_hash(payload.new_password)
    db.add(user)
    db.commit()
    return {"detail": "Password updated successfully"}
