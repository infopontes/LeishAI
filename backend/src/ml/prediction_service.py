# src/ml/prediction_service.py
import joblib
import pandas as pd
from pathlib import Path
from src.schemas.prediction import PredictionInput

# --- LIMIAR DE DECISÃO OTIMIZADO (do Notebook 11) ---
OPTIMAL_THRESHOLD = 0.2900
# --- FIM DO LIMIAR ---

# --- FUNÇÃO DE MAPEAMENTO REMOVIDA ---
# A função map_input_data foi removida. O modelo foi treinado
# diretamente nos dados brutos do CSV (ex: "Aumentados", "Alterada")
# e o nosso frontend já envia esses mesmos valores.
# --- FIM DA REMOÇÃO ---

class PredictionService:
    def __init__(self):
        """
        Loads the trained model and feature columns on service startup.
        """
        model_path = Path(__file__).parent.parent.parent / "ml_models"
        # Garante que estamos a carregar o modelo RandomForest (o que dá P(Neg)=80%)
        self.model = joblib.load(model_path / "leish_model_v1.joblib")
        self.training_columns = joblib.load(model_path / "training_columns_v1.joblib")

    def predict(self, input_data: PredictionInput) -> dict:
        """
        Prevê o diagnóstico usando o limiar otimizado de 2 níveis.
        """
        # --- LÓGICA DE PREDIÇÃO ATUALIZADA ---
        
        # 1. Converte os dados brutos (JSON) para um DataFrame
        # A função map_input_data foi removida.
        input_df = pd.DataFrame([input_data.model_dump()])

        # 2. One-Hot Encode o DataFrame (ex: cria 'linfonodos_Aumentados')
        input_encoded = pd.get_dummies(input_df)

        # 3. Alinha as colunas com os dados de treino (ex: encontra 'linfonodos_Aumentados')
        final_df = input_encoded.reindex(columns=self.training_columns, fill_value=0)

        # 4. Obter as probabilidades
        probabilities = self.model.predict_proba(final_df)[0]
        prob_negativo = probabilities[0]
        prob_positivo = probabilities[1]
        
        # 5. Aplicar o nosso limiar otimizado
        if prob_positivo > OPTIMAL_THRESHOLD:
            prediction_label = "Positivo"
            confidence = float(prob_positivo)
        else:
            prediction_label = "Negativo"
            confidence = float(prob_negativo) # Confiança de ser negativo

        return {"prediction": prediction_label, "confidence": confidence}
        # --- FIM DA LÓGICA ATUALIZADA ---

# Singleton instance of the service
prediction_service = PredictionService()