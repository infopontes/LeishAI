# src/ml/prediction_service.py

import joblib
import pandas as pd
import numpy as np  # <-- Import numpy
from pathlib import Path
from src.schemas.prediction import PredictionInput


class PredictionService:
    def __init__(self):
        model_path = Path(__file__).parent.parent.parent / "ml_models"
        self.model = joblib.load(model_path / "leish_model_v1.joblib")
        self.training_columns = joblib.load(
            model_path / "training_columns_v1.joblib"
        )

    def predict(self, input_data: PredictionInput) -> dict:
        """
        Preprocesses input data, makes a prediction, and returns the result
        along with the confidence score.
        """
        input_df = pd.DataFrame([input_data.model_dump()])
        input_encoded = pd.get_dummies(input_df)
        final_df = input_encoded.reindex(
            columns=self.training_columns, fill_value=0
        )

        # --- UPDATED LOGIC ---
        # Get the probabilities for each class [prob_neg, prob_pos]
        probabilities = self.model.predict_proba(final_df)

        # Get the confidence score (the highest probability)
        confidence = float(np.max(probabilities))

        # Get the predicted class index (0 for negative, 1 for positive)
        prediction_index = np.argmax(probabilities)

        # Map the index to the human-readable label
        prediction_label = "Positivo" if prediction_index == 1 else "Negativo"

        return {"prediction": prediction_label, "confidence": confidence}
        # --- END OF UPDATED LOGIC ---


prediction_service = PredictionService()
