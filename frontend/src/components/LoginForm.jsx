// src/components/LoginForm.jsx
import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { loginUser } from '../services/api';
import '../styles/LoginForm.css';

function LoginForm() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError('');
    setIsLoading(true);

    if (!email || !password) {
      setError(t('login.error.missingFields'));
      setIsLoading(false);
      return;
    }

    try {
      const data = await loginUser(email, password);
      console.log('Login successful:', data);

      localStorage.setItem('authToken', data.access_token);

      navigate('/predict');

    } catch (apiError) {
      setError(apiError.message || t('login.error.invalidCredentials'));
      console.error('Login failed:', apiError);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="login-form">
      {error && <p className="error-message">{error}</p>}
      <div className="form-group">
        <label htmlFor="email">{t('login.emailLabel')}</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          disabled={isLoading}
        />
      </div>
      <div className="form-group">
        <label htmlFor="password">{t('login.passwordLabel')}</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          disabled={isLoading}
        />
      </div>
      <button type="submit" className="submit-button" disabled={isLoading}>
        {isLoading ? t('login.loading') : t('menu.login')}
      </button>
    </form>
  );
}

export default LoginForm;