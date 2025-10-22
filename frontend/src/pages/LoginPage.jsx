// src/pages/LoginPage.jsx
import React from 'react';
import { useTranslation } from 'react-i18next';

function LoginPage() {
  const { t } = useTranslation();
  return (
    <div>
      <h2>{t('menu.login')}</h2>
      <p>Login form will go here.</p>
      {/* Add login form components later */}
    </div>
  );
}

export default LoginPage;