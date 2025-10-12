import sys
import os
import logging

# Configuração de Path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Imports dos nossos módulos de seed
from scripts.seeds import seed_breeds, seed_users # noqa: E402
from src.db.database import SessionLocal # noqa: E402

# Configuração do Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info(">>> Starting Database Seeding Process <<<")
    db = SessionLocal()
    try:
        # Altere de seed_roles_and_admin para seed_roles_and_users
        seed_users.seed_roles_and_users(db) # 👈 ALTERE ESTA LINHA
        seed_breeds.seed_breeds(db)
    except Exception as e:
        logger.error(f"An error occurred during seeding: {e}")
    finally:
        db.close()
    logger.info(">>> Database Seeding Process Finished <<<")


if __name__ == "__main__":
    main()