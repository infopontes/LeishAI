import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { resetPassword } from '../services/api';

import '../styles/ForgotPassword.css';

function ResetPasswordPage() {
  const { t } = useTranslation();
  const location = useLocation();
  const navigate = useNavigate();
  const [token, setToken] = useState('');
  const [password, setPassword] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const tokenFromUrl = params.get('token');
    if (tokenFromUrl) {
      setToken(tokenFromUrl);
    } else {
      setError(t('resetPassword.error.invalidToken'));
    }
  }, [location.search, t]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setMessage('');

    if (!password) {
      setError(t('resetPassword.error.missingPassword'));
      return;
    }
    if (password.length < 8) {
      setError(t('resetPassword.error.tooShort'));
      return;
    }
    if (!token) {
      setError(t('resetPassword.error.invalidToken'));
      return;
    }

    try {
      setIsSubmitting(true);
      await resetPassword(token, password);
      setMessage(t('resetPassword.success'));
      setTimeout(() => navigate('/login'), 1500);
    } catch (err) {
      setError(err.message || t('resetPassword.error.generic'));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="forgot-password-container">
      <div className="forgot-password-card">
        <h2>{t('resetPassword.title')}</h2>
        <p className="helper-text">{t('resetPassword.description')}</p>

        {message ? (
          <div className="success-message">{message}</div>
        ) : (
          <form onSubmit={handleSubmit} className="forgot-password-form">
            <label htmlFor="password">{t('resetPassword.passwordLabel')}</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              disabled={isSubmitting}
            />

            {error && <p className="error-message">{error}</p>}

            <button type="submit" disabled={isSubmitting}>
              {isSubmitting
                ? t('resetPassword.loading')
                : t('resetPassword.submit')}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

export default ResetPasswordPage;
