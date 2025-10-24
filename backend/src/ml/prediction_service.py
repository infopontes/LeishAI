# src/ml/prediction_service.py
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from src.schemas.prediction import PredictionInput

# --- INÍCIO DA ATUALIZAÇÃO ---
# Esta função mapeia os dados brutos do formulário para os dados limpos
# que o nosso modelo foi treinado para entender.
def map_input_data(input_data: PredictionInput) -> dict:
    """
    Maps raw frontend input data to the cleaned/standardized
    format that the model was trained on.
    """
    data = input_data.model_dump()
    
    # Mapeamentos para corrigir inconsistências (exatamente como no seed)
    lesion_mapping = {
        "Alterada": "Leves/Moderadas",
        "Aumentados": "Leves/Moderadas",
        "Grave": "Graves",
    }
    general_state_mapping = {"Moderado": "Regular", "Grave": "Ruim"}
    nutritional_state_mapping = {"Grave/Caquético": "Grave (Caquético)"}
    mucosa_color_mapping = {"Congesta": "Congesta (vermelho-escuro)"}

    # Aplica os mapeamentos
    # (Usamos .get() para aplicar o mapeamento ou manter o valor original se não estiver no mapa)
    data['general_state'] = general_state_mapping.get(data['general_state'], data['general_state'])
    data['nutritional_state'] = nutritional_state_mapping.get(data['nutritional_state'], data['nutritional_state'])
    data['coat'] = lesion_mapping.get(data['coat'], data['coat'])
    data['nails'] = lesion_mapping.get(data['nails'], data['nails'])
    data['lymph_nodes'] = lesion_mapping.get(data['lymph_nodes'], data['lymph_nodes'])
    data['mucosa_color'] = mucosa_color_mapping.get(data['mucosa_color'], data['mucosa_color'])

    # Os outros campos (como 'ectoparasites', 'blefarite', etc.)
    # já correspondem aos valores do Enum/treino, por isso não precisam de mapeamento.
    
    return data
# --- FIM DA ATUALIZAÇÃO ---


class PredictionService:
    def __init__(self):
        model_path = Path(__file__).parent.parent.parent / "ml_models"
        self.model = joblib.load(model_path / "leish_model_v1.joblib")
        self.training_columns = joblib.load(model_path / "training_columns_v1.joblib")

    def predict(self, input_data: PredictionInput) -> dict:
        """
        Preprocesses input data, makes a prediction, and returns the result
        along with the confidence score.
        """
        # --- INÍCIO DA ATUALIZAÇÃO ---
        # 1. Mapeia os dados brutos para dados limpos
        cleaned_data = map_input_data(input_data)
        
        # 2. Converte os dados limpos para um DataFrame
        input_df = pd.DataFrame([cleaned_data])
        # --- FIM DA ATUALIZAÇÃO ---

        # 3. One-Hot Encode o DataFrame limpo
        input_encoded = pd.get_dummies(input_df)

        # 4. Alinha as colunas com os dados de treino
        final_df = input_encoded.reindex(columns=self.training_columns, fill_value=0)

        # 5. Faz a predição
        probabilities = self.model.predict_proba(final_df)
        confidence = float(np.max(probabilities))
        prediction_index = np.argmax(probabilities)
        prediction_label = "Positivo" if prediction_index == 1 else "Negativo"
        
        return {"prediction": prediction_label, "confidence": confidence}

prediction_service = PredictionService()