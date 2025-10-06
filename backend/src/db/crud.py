from sqlalchemy.orm import Session
from . import models

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, email: str, password: str):
    # ATENÇÃO: Por enquanto, salvaremos a senha em texto plano.
    # Na próxima fase (API), vamos adicionar o hashing!
    fake_hashed_password = password + "_hashed" # Simulação
    db_user = models.User(email=email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user