import logging
from sqlalchemy.orm import Session
import src.db.crud.crud_role as crud_role
import src.db.crud.crud_user as crud_user
from src.schemas.role import RoleCreate
from src.schemas.user import UserCreate
from src.core.config import settings

logger = logging.getLogger(__name__)

ROLES_TO_CREATE = [
    {"name": "admin", "description": "System Administrator"},
    {"name": "veterinario", "description": "Veterinarian user"},
    {"name": "coordenador", "description": "Coordinator user"},
]


def seed_roles_and_users(db: Session) -> None:
    logger.info("--- Seeding Roles and Users ---")

    for role_data in ROLES_TO_CREATE:
        role = crud_role.get_role_by_name(db, name=role_data["name"])
        if not role:
            role_in = RoleCreate(
                name=role_data["name"], description=role_data["description"]
            )
            crud_role.create_role(db, role=role_in)
            logger.info(f"Created role: {role_data['name']}")
        else:
            logger.info(
                f"Role '{role_data['name']}' already exists. Skipping."
            )

    admin_role = crud_role.get_role_by_name(db, name="admin")

    # Create Administrator User
    admin_email = settings.DEFAULT_ADMIN_EMAIL
    admin_user = crud_user.get_user_by_email(db, email=admin_email)
    if not admin_user:
        user_in = UserCreate(
            email=admin_email,
            password=settings.DEFAULT_ADMIN_PASSWORD,
            full_name="Admin LeishAI",
            institution="LeishAI Project",
        )
        new_admin = crud_user.create_user(db, user=user_in)
        new_admin.role_id = admin_role.id
        new_admin.is_active = True
        db.commit()
        logger.info(f"Created AND activated admin user: {admin_email}")
    else:
        logger.info(f"Admin user '{admin_email}' already exists. Skipping.")

    # Create Veterinary user
    vet_email = settings.DEFAULT_VET_EMAIL
    vet_user = crud_user.get_user_by_email(db, email=vet_email)
    if not vet_user:
        user_in = UserCreate(
            email=vet_email,
            password=settings.DEFAULT_VET_PASSWORD,
            full_name="Marcelo Pontes",
            institution="UFPI",
        )
        new_vet = crud_user.create_user(db, user=user_in)
        new_vet.is_active = True
        db.commit()
        logger.info(f"Created AND activated veterinarian user: {vet_email}")
    else:
        logger.info(
            f"Veterinarian user '{vet_email}' already exists. Skipping."
        )

    logger.info("--- Finished Seeding Roles and Users ---")
