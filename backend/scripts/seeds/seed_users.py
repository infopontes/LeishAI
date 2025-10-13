import logging
from sqlalchemy.orm import Session
import src.db.crud.crud_role as crud_role
import src.db.crud.crud_user as crud_user
from src.schemas.role import RoleCreate
from src.schemas.user import UserCreate

logger = logging.getLogger(__name__)

# 1. Definir os perfis que queremos garantir que existam
ROLES_TO_CREATE = [
    {"name": "admin", "description": "System Administrator"},
    {"name": "veterinario", "description": "Veterinarian user"},
    {"name": "coordenador", "description": "Coordinator user"},
]


def seed_roles_and_users(db: Session) -> None:
    logger.info("--- Seeding Roles and Users ---")

    # 2. Criar Perfis (Roles) em um loop
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

    # Garante que temos o objeto 'admin_role' para a atribuição
    admin_role = crud_role.get_role_by_name(db, name="admin")

    # 3. Criar Usuário Administrador
    admin_email = "admin@dsleish.com"
    admin_user = crud_user.get_user_by_email(db, email=admin_email)
    if not admin_user:
        user_in = UserCreate(
            email=admin_email, password="leishmaniose@the!br343pi"
        )
        # A função create_user atribui 'veterinario' por padrão,
        # então precisamos sobrescrever com o perfil de admin.
        new_admin = crud_user.create_user(db, user=user_in)
        new_admin.role_id = admin_role.id
        db.commit()
        logger.info(f"Created admin user: {admin_email}")
    else:
        logger.info(f"Admin user '{admin_email}' already exists. Skipping.")

    # 4. Criar Usuário Veterinário
    vet_email = "infopontes@gmail.com"
    vet_user = crud_user.get_user_by_email(db, email=vet_email)
    if not vet_user:
        user_in = UserCreate(email=vet_email, password="delta@phbpi")
        # Aqui não precisamos fazer nada extra, pois a função 'create_user'
        # já atribui o perfil 'veterinario' por padrão.
        crud_user.create_user(db, user=user_in)
        logger.info(f"Created veterinarian user: {vet_email}")
    else:
        logger.info(
            f"Veterinarian user '{vet_email}' already exists. Skipping."
        )

    logger.info("--- Finished Seeding Roles and Users ---")
