// src/pages/LoginPage.jsx
import React from 'react';
import { useTranslation } from 'react-i18next';
import LoginForm from '../components/LoginForm'; // 👈 Import the form component
import '../styles/LoginPage.css';

function LoginPage() {
  const { t } = useTranslation();
  return (
    <div className="login-page">
      <h2>{t('menu.login')}</h2>
      <LoginForm /> {/* 👈 Use the form component here */}
    </div>
  );
}

export default LoginPage;
