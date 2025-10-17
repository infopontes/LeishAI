# src/schemas/prediction.py

from pydantic import BaseModel


# Schema for the input data required by the model
class PredictionInput(BaseModel):
    general_state: str | None = None
    ectoparasites: str | None = None
    nutritional_state: str | None = None
    coat: str | None = None
    nails: str | None = None
    mucosa_color: str | None = None
    muzzle_ear_lesion: str | None = None
    lymph_nodes: str | None = None
    blepharitis: str | None = None
    conjunctivitis: str | None = None
    alopecia: str | None = None
    bleeding: str | None = None
    skin_lesion: str | None = None
    muzzle_lip_depigmentation: str | None = None
    animal_sex: str | None = None
    breed_name: str | None = None


# Schema for the output data returned by the API
class PredictionOutput(BaseModel):
    diagnosis_prediction: str
    # --- NEW FIELD ---
    # The model's confidence in the prediction, as a value between 0.0 and 1.0
    confidence_score: float
