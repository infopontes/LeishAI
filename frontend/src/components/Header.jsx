// src/components/Header.jsx
import React from 'react';
import { useTranslation } from 'react-i18next';
import LanguageSwitcher from './LanguageSwitcher';
import '../styles/Header.css';

function Header() {
  const { t } = useTranslation();

  return (
    <header className="header">
      <nav className="nav">
        <div className="navLinks">
          <a href="/" className="navLink">{t('menu.home')}</a>
          <a href="/about" className="navLink">{t('menu.about')}</a>
          <a href="/login" className="navLink">{t('menu.login')}</a>
        </div>
        <LanguageSwitcher />
      </nav>
    </header>
  );
}

export default Header;