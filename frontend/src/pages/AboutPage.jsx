// src/pages/AboutPage.jsx
import React from 'react';
import { useTranslation } from 'react-i18next';

function AboutPage() {
  const { t } = useTranslation();
  return (
    <div>
      <h2>{t('menu.about')}</h2>
      <p>This is the About page for the LeishAI project.</p>
      {/* Add more content about the project here */}
    </div>
  );
}

export default AboutPage;