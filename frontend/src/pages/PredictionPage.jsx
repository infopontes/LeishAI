// src/pages/PredictionPage.jsx
import React from 'react';
import { useTranslation } from 'react-i18next';
import PredictionForm from '../components/PredictionForm'; // 👈 Import the form

function PredictionPage() {
  const { t } = useTranslation();

  return (
    <div>
      <h2>{t('prediction.title')}</h2>
      <p>{t('prediction.description')}</p>
      
      {/* Use the PredictionForm component */}
      <PredictionForm /> 

      {/* Optional: Display token for debugging */}
      {/* {localStorage.getItem('authToken') && <p style={{ marginTop: '30px', fontSize: '0.8em', color: 'grey' }}>User is authenticated.</p>} */}
    </div>
  );
}

export default PredictionPage;