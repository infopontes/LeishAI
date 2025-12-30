import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { requestPasswordReset } from '../services/api';

import '../styles/ForgotPassword.css';

function ForgotPasswordPage() {
  const { t } = useTranslation();
  const [email, setEmail] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [status, setStatus] = useState('idle'); // idle | success
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');

    if (!email) {
      setError(t('forgotPassword.error.missingEmail'));
      return;
    }

    try {
      setIsSubmitting(true);
      await requestPasswordReset(email);
      setStatus('success');
    } catch (err) {
      setError(t('forgotPassword.error.generic'));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="forgot-password-container">
      <div className="forgot-password-card">
        <h2>{t('forgotPassword.title')}</h2>
        <p className="helper-text">{t('forgotPassword.description')}</p>

        {status === 'success' ? (
          <div className="success-message">{t('forgotPassword.success')}</div>
        ) : (
          <form
            onSubmit={handleSubmit}
            className="forgot-password-form"
            noValidate
          >
            <label htmlFor="email">{t('login.emailLabel')}</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              disabled={isSubmitting}
            />

            {error && <p className="error-message">{error}</p>}

            <button type="submit" disabled={isSubmitting}>
              {isSubmitting
                ? t('forgotPassword.loading')
                : t('forgotPassword.submit')}
            </button>
          </form>
        )}

        <Link to="/login" className="back-link">
          {t('forgotPassword.backToLogin')}
        </Link>
      </div>
    </div>
  );
}

export default ForgotPasswordPage;
