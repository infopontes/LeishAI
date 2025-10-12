import logging
from sqlalchemy.orm import Session
import src.db.crud.crud_breed as crud_breed
from src.schemas.breed import BreedCreate

logger = logging.getLogger(__name__)

INITIAL_BREEDS = [
    "SRD (Sem Raça Definida)", "Poodle", "Pastor Alemão", "Rottweiler", 
    "Pitbull", "Yorkshire", "Pinscher", "Fila", "Labrador", "Cofap", 
    "Dogue Alemão", "Mestiço", "Fox Paulistinha", "Weimaraner", 
    "Shipdog", "Dálmata", "Sharpei", "Terrier", "Dachshund", "Lhasa Apso", 
    "American"
]

def seed_breeds(db: Session) -> None:
    logger.info("--- Seeding Breeds ---")
    for breed_name in INITIAL_BREEDS:
        breed = crud_breed.get_breed_by_name(db, name=breed_name)
        if not breed:
            breed_in = BreedCreate(name=breed_name)
            crud_breed.create_breed(db, breed=breed_in)
            logger.info(f"Created breed: {breed_name}")
        else:
            logger.info(f"Breed '{breed_name}' already exists. Skipping.")
    logger.info("--- Finished Seeding Breeds ---")