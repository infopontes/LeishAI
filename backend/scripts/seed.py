import sys
import os
import logging

# Path Configuration
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from scripts.seeds import seed_breeds, seed_users, seed_from_csv  # noqa: E402
from src.db.database import SessionLocal  # noqa: E402

# Logging Configuration
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info(">>> Starting Database Seeding Process <<<")
    db = SessionLocal()
    try:
        seed_users.seed_roles_and_users(db)
        seed_breeds.seed_breeds(db)
        seed_from_csv.seed_from_csv(db)
    except Exception as e:
        logger.error(f"An error occurred during seeding: {e}", exc_info=True)
    finally:
        db.close()
    logger.info(">>> Database Seeding Process Finished <<<")


if __name__ == "__main__":
    main()
