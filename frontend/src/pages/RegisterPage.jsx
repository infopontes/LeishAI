import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { registerUser } from '../services/api';
import '../styles/ForgotPassword.css';

function RegisterPage() {
  const { t } = useTranslation();
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [institution, setInstitution] = useState('');
  const [password, setPassword] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setMessage('');

    if (!fullName || !email || !password) {
      setError(t('register.error.missingFields'));
      return;
    }
    if (password.length < 8) {
      setError(t('register.error.tooShort'));
      return;
    }

    try {
      setIsSubmitting(true);
      await registerUser({ fullName, email, institution, password });
      setMessage(t('register.success'));
    } catch (err) {
      setError(err.message || t('register.error.generic'));
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="forgot-password-container">
      <div className="forgot-password-card">
        <h2>{t('register.title')}</h2>
        <p className="helper-text">{t('register.description')}</p>

        {message ? (
          <div className="success-message">{message}</div>
        ) : (
          <form onSubmit={handleSubmit} className="forgot-password-form">
            <label htmlFor="fullName">{t('register.fullName')}</label>
            <input
              id="fullName"
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              disabled={isSubmitting}
            />

            <label htmlFor="email">{t('login.emailLabel')}</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={isSubmitting}
            />

            <label htmlFor="institution">{t('register.institution')}</label>
            <input
              id="institution"
              type="text"
              value={institution}
              onChange={(e) => setInstitution(e.target.value)}
              disabled={isSubmitting}
            />

            <label htmlFor="password">{t('login.passwordLabel')}</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={isSubmitting}
            />

            {error && <p className="error-message">{error}</p>}

            <button type="submit" disabled={isSubmitting}>
              {isSubmitting
                ? t('register.loading')
                : t('register.submit')}
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

export default RegisterPage;
