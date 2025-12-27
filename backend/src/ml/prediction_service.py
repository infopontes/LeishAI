# src/ml/prediction_service.py
import joblib
import pandas as pd
from pathlib import Path
from src.schemas.prediction import PredictionInput

# --- LIMIAR DE DECISÃO ---
# Esta é a linha que faltava e causou o NameError.
# Estamos usando 0.5 como padrão para o novo modelo LR (V2).
OPTIMAL_THRESHOLD = 0.5 
# --- FIM ---

class PredictionService:
    def __init__(self):
        """
        Carrega o modelo, o scaler e as colunas na inicialização.
        """
        # 1. O caminho agora aponta para 'ml_models' (para bater com seu comando cp)
        model_path = Path(__file__).parent.parent.parent / "ml_models" 
        
        # 2. Carrega os 3 novos artefatos da V2
        self.model = joblib.load(model_path / "leish_model_v2.joblib")
        self.scaler = joblib.load(model_path / "data_scaler_v2.joblib") 
        self.training_columns = joblib.load(model_path / "training_columns_v2.joblib")

    def predict(self, input_data: PredictionInput) -> dict:
        """
        Prevê o diagnóstico usando o modelo LR + Scaler.
        """
        # 1. Converte os dados brutos (JSON) para um DataFrame
        input_df = pd.DataFrame([input_data.model_dump()])

        # 2. One-Hot Encode o DataFrame (CORRIGIDO: drop_first=False)
        input_encoded = pd.get_dummies(input_df, drop_first=False)

        # 3. Alinha as colunas com os dados de treino
        final_df = input_encoded.reindex(columns=self.training_columns, fill_value=0)

        # 4. [NOVO PASSO CRÍTICO] Escala os dados
        final_df_scaled = self.scaler.transform(final_df)

        # 5. Obter as probabilidades (usando os dados escalados)
        probabilities = self.model.predict_proba(final_df_scaled)[0]
        prob_negativo = probabilities[0]
        prob_positivo = probabilities[1]
        
        # 6. Aplicar o limiar (ex: 0.5)
        # Esta linha agora funcionará, pois OPTIMAL_THRESHOLD está definido
        if prob_positivo > OPTIMAL_THRESHOLD:
            prediction_label = "Positivo"
            confidence = float(prob_positivo)
        else:
            prediction_label = "Negativo"
            confidence = float(prob_negativo) 

        return {"prediction": prediction_label, "confidence": confidence}

# Singleton instance of the service
prediction_service = PredictionService()