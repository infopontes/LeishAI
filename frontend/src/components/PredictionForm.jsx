// src/components/PredictionForm.jsx
import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { makePrediction, getBreeds } from '../services/api';
import '../styles/PredictionForm.css';

// --- OPÇÕES DEFINITIVAS BASEADAS NO SEU CSV ---
const options = {
  general_state: ['Bom', 'Moderado', 'Grave', 'Ruim'],
  ectoparasites: ['Ausente', 'Leve', 'Grave'],
  nutritional_state: ['Adequado/Eutrófico', 'Leve a Moderado', 'Grave/Caquético'],
  coat: ['Normal', 'Leves/Moderadas', 'Grave'],
  nails: ['Normal', 'Alterada'],
  mucosa_color: ['Normal (Rosa-claro)', 'Levemente Hipercorada', 'Congesta'],
  presence_absence: ['Presente', 'Ausente'], // Grupo partilhado
  lymph_nodes: ['Normal', 'Aumentados'],
  conjunctivitis: ['Ausente', 'Presente', 'Ceratoconjuntivite Grave', 'Conjuntivite Leve'],
  skin_lesion: ['Ausente', 'Presente', 'Leve/Moderada', 'Grave/Generalizada'],
  animal_sex: ['M', 'F'],
  // breed_name é carregado dinamicamente
};

// Mapa para os campos do formulário para as chaves da API
const fieldApiMap = {
  generalState: 'general_state', ectoparasites: 'ectoparasites', nutritionalState: 'nutritional_state',
  coat: 'coat', nails: 'nails', mucosaColor: 'mucosa_color', muzzleEarLesion: 'muzzle_ear_lesion',
  lymphNodes: 'lymph_nodes', blepharitis: 'blepharitis', conjunctivitis: 'conjunctivitis',
  alopecia: 'alopecia', bleeding: 'bleeding', skinLesion: 'skin_lesion',
  muzzleLipDepigmentation: 'muzzle_lip_depigmentation', animalSex: 'animal_sex', breedName: 'breed_name',
};

// Mapa para os campos do formulário para os seus grupos de opções correspondentes
const fieldOptionGroupMap = {
    generalState: 'general_state',
    ectoparasites: 'ectoparasites',
    nutritionalState: 'nutritional_state',
    coat: 'coat',
    nails: 'nails',
    mucosaColor: 'mucosa_color',
    muzzleEarLesion: 'presence_absence',
    lymphNodes: 'lymph_nodes',
    blepharitis: 'presence_absence',
    conjunctivitis: 'conjunctivitis',
    alopecia: 'presence_absence',
    bleeding: 'presence_absence',
    skinLesion: 'skin_lesion',
    muzzleLipDepigmentation: 'presence_absence',
    animalSex: 'animal_sex',
    breedName: 'breed_name', // Chave especial para lógica dinâmica
};

function PredictionForm() {
  const { t } = useTranslation();
  
  // Estado inicial como string vazia para suportar o placeholder "-- Selecione --"
  const [formData, setFormData] = useState({
    generalState: '', ectoparasites: '', nutritionalState: '', coat: '',
    nails: '', mucosaColor: '', muzzleEarLesion: '', lymphNodes: '',
    blepharitis: '', conjunctivitis: '', alopecia: '', bleeding: '',
    skinLesion: '', muzzleLipDepigmentation: '', animalSex: '', breedName: '',
  });

  const [breeds, setBreeds] = useState([]);
  const [breedsLoading, setBreedsLoading] = useState(true);
  const [predictionResult, setPredictionResult] = useState(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Busca as raças da API quando o componente é montado
  useEffect(() => {
    const fetchBreeds = async () => {
      setBreedsLoading(true);
      setError('');
      try {
        const breedsData = await getBreeds();
        console.log("Breeds data received from API:", breedsData);
        if (Array.isArray(breedsData) && breedsData.length > 0) {
          const breedNames = breedsData.map(b => b.name);
          const uniqueBreeds = [...new Set(breedNames.filter(name => name && name.trim() !== ''))].sort();
          setBreeds(uniqueBreeds);
          // Define 'SRD (Sem Raça Definida)' como padrão se existir
          if (uniqueBreeds.includes('SRD (Sem Raça Definida)')) {
            setFormData(prev => ({...prev, breedName: 'SRD (Sem Raça Definida)'}));
          }
        } else {
          console.warn("No breeds data received. Using default list.");
          setBreeds(['SRD (Sem Raça Definida)']); // Fallback
        }
      } catch (err) {
        console.error("Failed to fetch breeds:", err);
        setError(t('prediction.error.fetchBreeds', 'Failed to load breeds.'));
        setBreeds(['SRD (Sem Raça Definida)']); // Fallback
      } finally {
        setBreedsLoading(false);
      }
    };
    fetchBreeds();
  }, [t]); // Dependência 't' para recarregar se o idioma mudar

  // Lida com a alteração de qualquer campo do formulário
  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData(prevState => ({ ...prevState, [name]: value }));
  };

  // Lida com a submissão do formulário
  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setPredictionResult(null);
    setIsLoading(true);

    const apiPayload = {};
    for (const formKey in formData) {
      const apiKey = fieldApiMap[formKey];
      if (!apiKey) continue;
      
      let value = formData[formKey];
      
      // Envia 'null' se o campo estiver vazio (ex: "-- Selecione --")
      apiPayload[apiKey] = value === '' ? null : value;
    }

    // Garante que todas as chaves esperadas pela API são enviadas (mesmo como null)
    for (const key in fieldApiMap) {
        const apiKey = fieldApiMap[key];
        if (!(apiKey in apiPayload)) {
            apiPayload[apiKey] = null;
        }
    }

    try {
      console.log("Sending payload to API:", apiPayload);
      const result = await makePrediction(apiPayload);
      setPredictionResult(result);
      console.log("Prediction received:", result);
    } catch (apiError) {
      setError(apiError.message || t('prediction.error.general'));
      console.error('Prediction failed:', apiError);
    } finally {
      setIsLoading(false);
    }
  };

  // Função auxiliar para obter a chave de tradução correta para as opções
  const getOptionTranslationKey = (groupKey, optionValue) => {
    const cleanOptionKey = optionValue.replace(/[\s/().-]/g, '_');
    return `options.${groupKey}.${cleanOptionKey}`;
  };

  return (
    <div>
      <form onSubmit={handleSubmit} className="prediction-form">
        {/* Renderiza todos os campos do formulário dinamicamente */}
        {Object.keys(fieldApiMap).map((formKey) => {
          const apiKey = fieldApiMap[formKey];
          const label = t(`prediction.fields.${apiKey}`);
          const optionGroupKey = fieldOptionGroupMap[formKey];

          if (optionGroupKey === 'breed_name') {
            // --- Renderização especial para Raças (dinâmico) ---
            return (
              <div className="form-group" key={formKey}>
                <label htmlFor={formKey}>{label}</label>
                <select id={formKey} name={formKey} value={formData[formKey]} onChange={handleChange} disabled={isLoading || breedsLoading}>
                  <option value="">{t('options.select', '-- Select --')}</option>
                  {breedsLoading ? (
                    <option disabled>{t('loading.breeds', 'Loading breeds...')}</option>
                  ) : (
                    breeds.map(opt => <option key={opt} value={opt}>{opt}</option>)
                  )}
                </select>
              </div>
            );
          } else if (optionGroupKey) {
            // --- Renderização para todas as outras caixas de seleção ---
            const optionList = options[optionGroupKey] || [];
            return (
              <div className="form-group" key={formKey}>
                <label htmlFor={formKey}>{label}</label>
                <select id={formKey} name={formKey} value={formData[formKey]} onChange={handleChange} disabled={isLoading}>
                  <option value="">{t('options.select', '-- Select --')}</option>
                  {optionList.map(opt => (
                    <option key={opt} value={opt}>
                      {t(getOptionTranslationKey(optionGroupKey, opt), opt)}
                    </option>
                  ))}
                </select>
              </div>
            );
          } else {
             // Fallback para campos de texto (não deve ser usado com o mapa atual)
             return (
               <div className="form-group" key={formKey}>
                 <label htmlFor={formKey}>{label}</label>
                 <input type="text" id={formKey} name={formKey} value={formData[formKey]} onChange={handleChange} disabled={isLoading} />
               </div>
             );
          }
        })}

        <button type="submit" className="submit-button" disabled={isLoading || breedsLoading}>
          {isLoading ? t('prediction.loading') : t('prediction.submitButton')}
        </button>
      </form>

      {/* Exibição dos Resultados */}
      {error && <p className="error-message">{error}</p>}
      {predictionResult && (
        <div className="results-display">
          <h3>{t('prediction.resultTitle')}</h3>
          <p>
            {t('prediction.diagnosis')}:
            <span className={predictionResult.diagnosis_prediction === 'Positivo' ? 'positive' : 'negative'}>
              {t(`diagnosis.${predictionResult.diagnosis_prediction}`)}
            </span>
          </p>
          <p>
            {t('prediction.confidence')}:
            <span>{(predictionResult.confidence_score * 100).toFixed(1)}%</span>
          </p>
        </div>
      )}
    </div>
  );
}

export default PredictionForm;