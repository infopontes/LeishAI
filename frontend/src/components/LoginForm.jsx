import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { Link, useNavigate } from 'react-router-dom';
import { FaUser, FaLock } from 'react-icons/fa';

import { loginUser } from '../services/api';
import { useAuth } from '../context/AuthContext';

import '../styles/LoginForm.css';

function LoginForm() {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { login } = useAuth();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // 🔹 Load remembered email
  useEffect(() => {
    const savedEmail = localStorage.getItem('rememberedEmail');
    if (savedEmail) {
      setEmail(savedEmail);
      setRememberMe(true);
    }
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!email || !password) {
      setError(t('login.error.missingFields'));
      return;
    }

    try {
      setIsLoading(true);

      const data = await loginUser(email, password);
      login(data.access_token, rememberMe);

      navigate('/');
    } catch (err) {
      setError(
        err.message === 'INVALID_CREDENTIALS'
          ? t('login.error.invalidCredentials')
          : err.message
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} noValidate className="login-form">
      {error && <p className="error-message">{error}</p>}

      {/* Email */}
      <div className="form-group">
        <label htmlFor="email">{t('login.emailLabel')}</label>
        <div className="input-wrapper">
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={isLoading}
          />
          <FaUser className="icon" />
        </div>
      </div>

      {/* Password */}
      <div className="form-group">
        <label htmlFor="password">{t('login.passwordLabel')}</label>
        <div className="input-wrapper">
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            disabled={isLoading}
          />
          <FaLock className="icon" />
        </div>
      </div>

      {/* Remember me / Forgot password */}
      <div className="login-options">
        <label className="remember-me">
          <input
            type="checkbox"
            checked={rememberMe}
            onChange={(e) => setRememberMe(e.target.checked)}
            disabled={isLoading}
          />
          {t('login.rememberMe')}
        </label>

        <Link to="/forgot-password" className="forgot-password">
          {t('login.forgotPassword')}
        </Link>
      </div>

      {/* Submit */}
      <button type="submit" className="submit-button" disabled={isLoading}>
        {isLoading ? t('login.loading') : t('menu.login')}
      </button>
    </form>
  );
}

export default LoginForm;
