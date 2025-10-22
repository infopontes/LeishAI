// src/components/Header.jsx
import React from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import LanguageSwitcher from './LanguageSwitcher';
import '../styles/Header.css';

function Header() {
  const { t } = useTranslation();

  return (
    <header className="header">
      <nav className="nav">
        <div className="navLinks">
          <Link to="/" className="navLink">{t('menu.home')}</Link>
          <Link to="/about" className="navLink">{t('menu.about')}</Link>
          <Link to="/login" className="navLink">{t('menu.login')}</Link>
        </div>
        <LanguageSwitcher />
      </nav>
    </header>
  );
}

export default Header;