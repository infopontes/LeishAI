import csv
import logging
from sqlalchemy.orm import Session
from pathlib import Path

import src.db.crud.crud_owner as crud_owner
import src.db.crud.crud_breed as crud_breed
import src.db.crud.crud_animal as crud_animal
import src.db.crud.crud_assessment as crud_assessment
import src.db.crud.crud_user as crud_user
from src.schemas import owner as owner_schema
from src.schemas import breed as breed_schema
from src.schemas import animal as animal_schema
from src.schemas import assessment as assessment_schema

logger = logging.getLogger(__name__)


def map_clinical_data(row: dict) -> dict:
    """
    Mapeia e limpa os dados clínicos do CSV para corresponder aos nossos Enums e modelos.
    """
    lesion_mapping = {
        "Alterada": "Leves/Moderadas",
        "Aumentados": "Leves/Moderadas",
        "Grave": "Graves",
    }
    general_state_mapping = {"Moderado": "Regular", "Grave": "Ruim"}
    nutritional_state_mapping = {"Grave/Caquético": "Grave (Caquético)"}
    mucosa_color_mapping = {"Congesta": "Congesta (vermelho-escuro)"}

    mapped_data = {
        "general_state": general_state_mapping.get(
            row.get("estado_geral"), row.get("estado_geral")
        )
        or None,
        "ectoparasites": row.get("ectoparas") or None,
        "nutritional_state": nutritional_state_mapping.get(
            row.get("est_nutri"), row.get("est_nutri")
        )
        or None,
        "coat": lesion_mapping.get(row.get("pelagem"), row.get("pelagem"))
        or None,
        "nails": lesion_mapping.get(row.get("unhas"), row.get("unhas"))
        or None,
        "mucosa_color": mucosa_color_mapping.get(
            row.get("color_mucosa"), row.get("color_mucosa")
        )
        or None,
        "muzzle_ear_lesion": row.get("lesao_focinho_orelha") or None,
        "lymph_nodes": lesion_mapping.get(
            row.get("linfonodos"), row.get("linfonodos")
        )
        or None,
        "blepharitis": row.get("blefarite") or None,
        "conjunctivitis": row.get("conjuntivite") or None,
        "alopecia": row.get("alopecia") or None,
        "bleeding": row.get("sangramento") or None,
        "skin_lesion": row.get("lesao_de_pele") or None,
        "muzzle_lip_depigmentation": row.get("despigmentacao_focinho_labio")
        or None,
        "culture": row.get("cultura") or None,
        "slide": row.get("lamina") or None,
        "diagnosis": row.get("diagnostico") or None,
    }
    return mapped_data


def seed_from_csv(db: Session) -> None:
    logger.info("--- Seeding data from CSV file ---")

    default_user = crud_user.get_user_by_email(
        db, email="infopontes@gmail.com"
    )
    if not default_user:
        logger.error(
            "Default user 'infopontes@gmail.com' not found. Please run user seed first."
        )
        return

    default_owner_name = "Marcelo Pontes Rodrigues"
    default_owner = crud_owner.get_owner_by_name(db, name=default_owner_name)
    if not default_owner:
        logger.info(
            f"Default owner '{default_owner_name}' not found, creating..."
        )
        default_owner_in = owner_schema.OwnerCreate(
            name=default_owner_name,
            phone="+5586994244568",
            address="Rua A",
            neighborhood="Reis Veloso",
            city="Parnaíba",
            state="PI",
        )
        default_owner = crud_owner.create_owner(db, owner=default_owner_in)
        logger.info("Default owner created successfully.")
    else:
        logger.info(f"Default owner '{default_owner_name}' found.")

    csv_file_path = (
        Path(__file__).resolve().parent.parent.parent / "dataset.csv"
    )

    # We added diagnostic logging
    try:
        with open(csv_file_path, mode="r", encoding="latin-1") as csvfile:
            # Load all lines into memory first
            reader = list(csv.DictReader(csvfile, delimiter=";"))
            total_rows = len(reader)
            logger.info(
                f"Found {total_rows} rows in CSV file. Starting import..."
            )

            # Now iterate over the list of lines
            for i, row in enumerate(reader):
                # Print progress every 50 lines
                if (i + 1) % 50 == 0:
                    logger.info(f"Processing row {i + 1}/{total_rows}...")

                if not row.get("id_db_original"):
                    continue

                # Owner's Logic
                owner_name_from_csv = row.get("proprietario")
                if owner_name_from_csv and owner_name_from_csv.strip():
                    owner = crud_owner.get_owner_by_name(
                        db, name=owner_name_from_csv
                    )
                    if not owner:
                        owner_in = owner_schema.OwnerCreate(
                            name=owner_name_from_csv
                        )
                        owner = crud_owner.create_owner(db, owner=owner_in)
                else:
                    owner = default_owner

                # Logic of Race
                breed_name = row.get("raca") or "SRD (Sem Raça Definida)"
                breed = crud_breed.get_breed_by_name(db, name=breed_name)
                if not breed:
                    breed_in = breed_schema.BreedCreate(name=breed_name)
                    breed = crud_breed.create_breed(db, breed=breed_in)

                # Animal Logic
                animal_original_id = row["id_db_original"]
                animal = crud_animal.get_animal_by_original_id(
                    db, original_id=animal_original_id
                )
                if not animal:
                    animal_in = animal_schema.AnimalCreate(
                        name=row.get("nome") or "Nome Não Informado",
                        original_id=animal_original_id,
                        sex=row.get("sexo"),
                        owner_id=owner.id,
                        breed_id=breed.id,
                    )
                    animal = crud_animal.create_animal(db, animal=animal_in)

                # Creation of Service
                clinical_data = map_clinical_data(row)
                assessment_in = assessment_schema.AssessmentCreate(
                    animal_id=animal.id, **clinical_data
                )
                crud_assessment.create_assessment(
                    db, assessment=assessment_in, user_id=default_user.id
                )

        logger.info(f"Successfully processed {total_rows} rows.")

    except FileNotFoundError:
        logger.error(f"CSV file not found at path: {csv_file_path}")
    except Exception as e:
        logger.error(
            f"An unexpected error occurred during CSV processing: {e}",
            exc_info=True,
        )

    logger.info("--- Finished seeding from CSV ---")
