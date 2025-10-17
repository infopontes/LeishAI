# src/api/v1/router_prediction.py

from fastapi import APIRouter, Depends
from src.schemas import prediction as prediction_schema
from src.ml.prediction_service import prediction_service
from .dependencies import get_current_user

router = APIRouter(prefix="/predict", tags=["Prediction"])


@router.post(
    "/",
    response_model=prediction_schema.PredictionOutput,
    dependencies=[Depends(get_current_user)],
)
def make_diagnosis_prediction(input_data: prediction_schema.PredictionInput):
    """
    Receives clinical and animal data and returns a diagnosis prediction
    with a confidence score.
    """
    result = prediction_service.predict(input_data)

    # --- UPDATED RETURN ---
    return {
        "diagnosis_prediction": result["prediction"],
        "confidence_score": result["confidence"],
    }
