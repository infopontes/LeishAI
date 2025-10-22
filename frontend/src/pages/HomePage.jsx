// src/pages/HomePage.jsx
import React from 'react';
import { useTranslation } from 'react-i18next';

function HomePage() {
  const { t } = useTranslation();
  return (
    <div style={{ textAlign: 'center' }}>
      <h1>{t('greeting')}</h1>
      <img 
        src="/images/dsleish-hero.png" 
        alt="DSLeish main visual" 
        className="heroImage"
      />
    </div>
  );
}

export default HomePage;